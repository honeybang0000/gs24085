import os
import gradio as gr


# 1. 간단한 테스트용 함수 (여기에 나중에 회원님의 AI 모델 코드를 연결하면 됩니다)
def greet(name):
    return f"안녕하세요 {name}님! Render 배포에 성공하셨습니다! 🎉"


# 2. Gradio 웹 화면 레이아웃 디자인
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 나의 첫 AI 웹 서버")

    with gr.Row():
        name_input = gr.Textbox(label="이름을 입력하세요", placeholder="홍길동")
        output_text = gr.Textbox(label="결과")

    submit_btn = gr.Button("실행하기")

    # 버튼을 누르면 greet 함수가 실행되도록 연결
    submit_btn.click(fn=greet, inputs=name_input, outputs=output_text)

# 3. Render 서버 환경에 맞춰 포트 설정 후 실행
if __name__ == "__main__":
    # Render는 PORT 환경 변수를 제공하므로, 이를 읽어서 서버를 엽니다.
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)