# pairwise-color-grading-lut

同一段素材在调色台和播放器里颜色完全不同，LUT 在 log 空间生成，播放器却把编码值直接当线性输入；3D LUT 用三线性插值，纯色块边缘出现三角面片，肤色过渡断层；LUT 尺寸 17 在暗部色阶不够，黑场出现一圈圈同心圆；超出域外的颜色被钳到边界，霓虹灯变成纯红；带 alpha 的素材在 LUT 之后合成，半透明边缘出现彩边；HDR 素材先做了色调映射再套 LUT，高光细节被压掉两次；CDL 斜率与 LUT 同时应用，顺序反了导致整体偏绿；LUT 缓存按文件路径做键，替换同名文件后仍在用旧表；sRGB 与 Rec.709 的传递函数不同，套用后中间调整体偏亮；LUT 只在 8bit 纹理上采样，10bit 素材出现 banding。render/color_grading_lut.py 是核心，tests/test_color_grading_lut.py 15个红。要修的是：统一在线性空间；四面体插值；按域分段尺寸；域外软映射；alpha 后合成；只映射一次；CDL 在 LUT 前；缓存带哈希；按色彩空间选表；浮点纹理采样。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：见平台；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
