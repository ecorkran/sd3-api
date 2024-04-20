import gradio as gr


class HomePage:

    @staticmethod
    def launchUI(uifn, serverName=None, serverPort=None):
        # Define your Gradio interface
        inputComponents = [
            gr.Textbox(label="Prompt"),
            gr.Textbox(label="Negative Prompt"),
            gr.Dropdown(choices=['16:9', '4:3', '1:1'], label="Aspect Ratio", value="16:9"),
            gr.Radio(choices=['png', 'jpg'], label="Image Format", value="png"),
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

