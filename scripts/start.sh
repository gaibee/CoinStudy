nohup uvicorn main:app --host 0.0.0.0 --port 5004 --reload > server.log 2>&1 &
echo "서버를 실행했습니다."