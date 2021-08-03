from datetime import datetime, timezone
import re

TAG_RE = re.compile(r'<[^>]+>')

def datetime_now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat()


def remove_tags(text):
    return TAG_RE.sub('', text)
