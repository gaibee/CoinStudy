from jinja2 import Template

template = Template("""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
        <title>{{ title }}</title>
    <style>
        body { font-family: sans-serif; background: #f9f9f9; padding: 0; margin: 0; }
        header { background: #4CAF50; color: white; padding: 1rem; text-align: center; font-weight: bold; }
        main { padding: 2rem; }
        <!-- style 태그 안에 추가(또는 별도 css 로 분리) -->
        body {
            font-family: 'Noto Sans KR', sans-serif;
        }
    </style>
    <!-- head 태그 안에 추가 -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap" rel="stylesheet">

</head>
<body>
    <header>사이트 제목을 입력하는 구간</header>
    <main>
        {{ content | safe }}
    </main>
</body>
</html>
""")

def render_with_layout(content: str, title: str = "대시보드"):
    return template.render(title=title, content=content)