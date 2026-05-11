"""
模板数据服务：Round 0 返回写死在代码中的示例模板。
后续可从 JSON/YAML 或数据库读取，并保持同一套结构。
"""

from copy import deepcopy

# Mock 模板：与 frontend/src/types/template.ts 概念一致（字段名后端用 snake_case 也可，
# Round 0 为方便与示例 JSON 对照，图层内保留 camelCase 子字段）。
MOCK_TEMPLATES: list[dict] = [
    {
        "id": "vertical_short_video_v1",
        "name": "竖屏短视频模板 V1",
        "canvas": {"width": 1080, "height": 1920, "fps": 30},
        "layers": [
            {
                "type": "video",
                "role": "main",
                "x": 0,
                "y": 0,
                "width": 1080,
                "height": 1920,
                "zIndex": 0,
            },
            {
                "type": "video",
                "role": "pip",
                "x": 760,
                "y": 120,
                "width": 260,
                "height": 360,
                "zIndex": 10,
            },
            {
                "type": "text",
                "role": "title",
                "x": 80,
                "y": 120,
                "width": 920,
                "height": 160,
                "fontSize": 64,
                "color": "#FFFFFF",
                "align": "center",
                "zIndex": 20,
            },
            {
                "type": "text",
                "role": "subtitle",
                "x": 80,
                "y": 300,
                "width": 920,
                "height": 120,
                "fontSize": 40,
                "color": "#EEEEEE",
                "align": "center",
                "zIndex": 21,
            },
            {
                "type": "text",
                "role": "caption",
                "x": 60,
                "y": 1600,
                "width": 960,
                "height": 200,
                "fontSize": 36,
                "color": "#FFFFFF",
                "align": "left",
                "zIndex": 22,
            },
            {
                "type": "text",
                "role": "labels",
                "x": 80,
                "y": 1780,
                "width": 920,
                "height": 100,
                "fontSize": 28,
                "color": "#FFD54F",
                "align": "left",
                "zIndex": 23,
            },
        ],
    },
    {
        "id": "horizontal_highlight_v1",
        "name": "横屏精华切片 V1",
        "canvas": {"width": 1920, "height": 1080, "fps": 30},
        "layers": [
            {
                "type": "video",
                "role": "main",
                "x": 0,
                "y": 0,
                "width": 1920,
                "height": 1080,
                "zIndex": 0,
            },
            {
                "type": "text",
                "role": "title",
                "x": 80,
                "y": 60,
                "width": 1760,
                "height": 120,
                "fontSize": 72,
                "color": "#FFFFFF",
                "align": "left",
                "zIndex": 10,
            },
        ],
    },
]


def list_templates() -> list[dict]:
    """返回模板列表的深拷贝，避免调用方意外修改全局 Mock。"""
    return deepcopy(MOCK_TEMPLATES)


def get_template_by_id(template_id: str) -> dict | None:
    """按 ID 查找模板；找不到返回 None。"""
    for t in MOCK_TEMPLATES:
        if t["id"] == template_id:
            return deepcopy(t)
    return None

