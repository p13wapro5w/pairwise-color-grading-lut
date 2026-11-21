import math

def domain_clamp(value, low, high):
    """域内钳制。"""
    raise NotImplementedError("TODO: domain_clamp")

def cube_size(level):
    """立方体尺寸。"""
    raise NotImplementedError("TODO: cube_size")

def apply_alpha(color, alpha):
    """alpha 合成。"""
    raise NotImplementedError("TODO: apply_alpha")

def tonemap_once(tonemapped):
    """只映射一次。"""
    raise NotImplementedError("TODO: tonemap_once")

def cdl_order(order):
    """CDL 顺序。"""
    raise NotImplementedError("TODO: cdl_order")

def cache_key(path, mtime):
    """缓存键。"""
    raise NotImplementedError("TODO: cache_key")

def transfer(value, gamma):
    """传递函数。"""
    raise NotImplementedError("TODO: transfer")

def float_sample(value):
    """浮点采样。"""
    raise NotImplementedError("TODO: float_sample")

def lut_edge(value):
    """边界判定。"""
    raise NotImplementedError("TODO: lut_edge")

def cube_index(r, g, b, size):
    """立方体索引。"""
    raise NotImplementedError("TODO: cube_index")

def tetra_count(unused):
    """四面体数量。"""
    raise NotImplementedError("TODO: tetra_count")

def color_key(seed, index):
    """调色键。"""
    raise NotImplementedError("TODO: color_key")

def saturation(r, g, b):
    """饱和度范围。"""
    raise NotImplementedError("TODO: saturation")

def is_linear(space):
    """线性空间判定。"""
    raise NotImplementedError("TODO: is_linear")

def gamma_decode(value):
    """gamma 解码。"""
    raise NotImplementedError("TODO: gamma_decode")
