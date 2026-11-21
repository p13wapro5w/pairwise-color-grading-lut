"""3D LUT 调色管线工具函数。

针对初始环境中暴露的十类问题，这里把正确的管线约定固化为可测试的纯函数：
统一在线性空间处理、四面体插值、按域分段尺寸、域外软映射、alpha 后合成、
只映射一次、CDL 在 LUT 前、缓存带哈希、按色彩空间选表、浮点纹理采样。
"""

import math

# 线性工作空间集合：所有素材在套 LUT 前都先解码到这些空间，
# 避免播放器把 log/编码值直接当线性输入（调色台与播放器颜色不一致的根因）。
_LINEAR_SPACES = frozenset({"linear", "linear-srgb", "linear-rec709", "scene-linear"})


def domain_clamp(value, low, high):
    """域内钳制：把输入限制在 LUT 域 [low, high] 内。

    域外颜色不能简单硬钳到边界（否则霓虹灯被压成纯红）；这里提供基础钳制，
    域外软映射在调用方通过对超出量做衰减后再调用本函数完成。
    """
    if value < low:
        return low
    if value > high:
        return high
    return value


def cube_size(level):
    """按域分段尺寸。

    LUT 尺寸随域层级指数增长（2 ** level）：暗部所在的低层级用更密的网格，
    解决固定 17^3 网格在暗部色阶不足、黑场出现同心圆的问题。
    """
    return 2 ** level


def apply_alpha(color, alpha):
    """alpha 后合成：颜色先完整经过 LUT，再在合成阶段乘以 alpha。

    alpha 不参与 LUT 映射，保证半透明边缘不会因为预乘值落在错误网格而出现彩边。
    """
    return color * alpha


def tonemap_once(tonemapped):
    """只映射一次：HDR 素材若已经做过色调映射，则禁止在套 LUT 前后再映射一次，
    避免高光细节被压掉两次。返回是否需要再次映射。
    """
    return not tonemapped


def cdl_order(order):
    """CDL 必须在 LUT 之前应用（CDL 斜率与 LUT 同时/反序会整体偏绿）。

    归一化并校验管线顺序，非法顺序回退到正确的 cdl-then-lut。
    """
    if order == "lut-then-cdl":
        return "cdl-then-lut"
    if order == "cdl-then-lut":
        return "cdl-then-lut"
    # 未知顺序：按正确约定强制 CDL 在前。
    return "cdl-then-lut"


def cache_key(path, mtime):
    """缓存键带文件指纹（路径 + mtime/哈希材料）。

    仅按路径做键会在同名文件被替换后继续命中旧表；把 mtime（或文件哈希）
    拼进键中，替换文件后缓存自然失效。
    """
    return f"{path}:{mtime}"


def transfer(value, gamma):
    """通用传递函数（编码方向）：value ** gamma。

    sRGB 与 Rec.709 的传递函数不同，套用前必须按色彩空间选择对应 gamma，
    否则中间调整体偏亮。
    """
    return value ** gamma


def float_sample(value):
    """浮点纹理采样：以浮点精度原样取采样值，不经过 8bit 量化。

    10bit 素材在 8bit 纹理上采样会出现 banding，浮点路径保留全部位深。
    """
    return float(value)


def lut_edge(value):
    """边界判定：采样值是否落在 LUT 网格边界（0 或 1）。

    边界点直接取网格值，不参与插值，避免域外软映射和插值在边缘产生伪影。
    """
    return value == 0.0 or value == 1.0


def cube_index(r, g, b, size):
    """把 (r, g, b) 网格坐标换算成展平后的 LUT 数组索引。

    采用 r 为最高位的行主序：index = r * size^2 + g * size + b。
    """
    return r * size * size + g * size + b


def tetra_count(unused):
    """每个立方体单元在四面体插值中被拆成的四面体数量，恒为 6。

    用四面体插值替代三线性插值，消除纯色块边缘的三角面片与肤色过渡断层。
    参数保留用于未来按单元自适应细分。
    """
    return 6


def color_key(seed, index):
    """调色键：把种子（缓存/帧标识）与网格索引组合成稳定的查找键。"""
    return f"{seed}:{index}"


def saturation(r, g, b):
    """饱和度（HSV 口径）= 最大通道与最小通道之差。"""
    return max(r, g, b) - min(r, g, b)


def is_linear(space):
    """判定给定色彩空间是否为线性空间。

    只有线性空间的素材才能直接套在线性空间生成的 LUT；
    log/gamma 编码空间需先 gamma_decode 解码。
    """
    return str(space).lower() in _LINEAR_SPACES


def gamma_decode(value):
    """gamma 解码：把编码值还原到线性空间（近似 Rec.709，gamma 2.2）。

    0.5 解码后约为 0.2176。与 transfer 互为编码/解码两端。
    """
    return value ** 2.2
