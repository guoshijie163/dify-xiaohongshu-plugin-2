import json
import requests
from typing import Dict, Any, Optional

def fetch_xiaohongshu_note(note_id: Optional[str] = None, share_url: Optional[str] = None) -> Dict[str, Any]:
    """
    获取小红书笔记数据的Dify工具函数
    
    参数:
        note_id: 小红书笔记ID
        share_url: 小红书笔记分享链接
        
    返回:
        包含笔记数据或错误信息的字典
    """
    try:
        # 参数验证
        if not note_id and not share_url:
            return {
                "status": "error",
                "message": "请提供笔记ID(note_id)或分享链接(share_url)"
            }
            
        # 如果提供了分享链接，从链接中提取笔记ID
        if share_url and not note_id:
            note_id = extract_note_id(share_url)
            if not note_id:
                return {
                    "status": "error",
                    "message": "无法从分享链接中提取笔记ID"
                }
        
        # 构建URL和请求参数
        url = "https://api.tikhub.io/api/v1/xiaohongshu/web_v2/fetch_feed_notes"
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer kIcrb2144Us7jDAt2DazvXQL8ztSt6rBkI5X6A3HujBt0nRYWtpo1A7nPg=='
        }
        params = {
            'note_id': note_id
        }
        
        # 发送API请求
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "请求超时，请稍后重试"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"网络请求失败: {str(e)}"
            }
        
        # 处理响应数据
        try:
            json_data = response.json()
            
            # 检查API返回状态
            if json_data.get('code') != 200:
                return {
                    "status": "error",
                    "message": json_data.get('message', '请求失败')
                }
            
            # 获取笔记列表
            note_list = json_data.get('data', {}).get('note_list', [])
            
            if not note_list:
                return {
                    "status": "error",
                    "message": "未找到笔记数据"
                }
            
            # 格式化笔记数据
            formatted_notes = []
            for note in note_list:
                formatted_note = {
                    'note_id': note.get('id', ''),
                    'title': note.get('title', 'No Title'),
                    'author': {
                        'user_id': note['user'].get('userid', ''),
                        'nickname': note['user'].get('nickname', ''),
                        'avatar': note['user'].get('image', '')
                    },
                    'content': {
                        'text': note.get('desc', ''),
                        'images': [img.get('url', '') for img in note.get('images_list', [])],
                        'video': None  # 当前返回数据中没有视频字段
                    },
                    'statistics': {
                        'likes': note.get('liked_count', 0),
                        'collects': note.get('collected_count', 0),
                        'comments': note.get('comments_count', 0),
                        'shares': note.get('shared_count', 0)
                    },
                    'time': note.get('time', ''),
                    'url': note.get('share_info', {}).get('link', f"https://www.xiaohongshu.com/discovery/item/{note.get('id', '')}")
                }
                formatted_notes.append(formatted_note)
            
            return {
                "status": "success",
                "data": {
                    "notes": formatted_notes,
                    "total": len(formatted_notes)
                }
            }
            
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "解析响应数据失败"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"处理失败: {str(e)}"
        }

def extract_note_id(share_url: str) -> Optional[str]:
    """从分享链接中提取笔记ID"""
    import re
    pattern = r'/(\w+)(?:\?|$)'
    match = re.search(pattern, share_url)
    return match.group(1) if match else None

# Dify工具函数定义
def get_xiaohongshu_note(note_id=None, share_url=None):
    """
    获取小红书笔记内容
    
    参数:
        note_id: 笔记ID
        share_url: 分享链接
    
    返回:
        小红书笔记内容
    """
    result = fetch_xiaohongshu_note(note_id, share_url)
    return result
