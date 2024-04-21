import gradio as gr


class HomePage:

    @staticmethod
    def launchUI(uifn, serverName=None, serverPort=None):
        # Define your Gradio interface
        inputComponents = [
            gr.Textbox(label="Prompt"),
            gr.Textbox(label="Negative Prompt"),
            gr.Dropdown(choices=['21:9', '16:9', '5:4', '3:2', '1:1', '2:3', '4:5', '9:16', '9:21' ], label="Aspect Ratio", value="16:9"),
            gr.Radio(choices=['png', 'jpg'], label="Image Format", value="png"),
            gr.Radio(choices=['sd3', 'sd3-turbo'], label="Model", value="sd3"),
            gr.Textbox(label="Seed", value="0"),
        ]

        outputComponents = [
            gr.Image(type="pil", label="Generated Image"),
            gr.Textbox(label="Seed"),
        ]

        demo = gr.Interface(
            fn=uifn,
            inputs=inputComponents,
            outputs=outputComponents,
            title="SD3 Image Generator",
            description="Enter a prompt and optional negative prompt to generate an image."
        )

        demo.launch(server_name=serverName, server_port=serverPort)

