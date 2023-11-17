import nextcord, io
from gtts import gTTS





class AnswerButton(nextcord.ui.View):
    def __init__(self, actual_answer):
        super().__init__(timeout=60)
        self.add_item(nextcord.ui.Button(label="Invite me to your server", url="https://nomindustries.com/SV/invite"))
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url="https://nomindustries.com/SV/privacy"))
        self.actual_answer = actual_answer
        self.answer = "Too Long ---------------"
        self.audio_sent = False

    @nextcord.ui.button(label = "Answer", style = nextcord.ButtonStyle.green, disabled=False)
    async def answer_ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        answerinput = AnswerModal()
        await interaction.response.send_modal(answerinput)
        await answerinput.wait()
        self.answer = answerinput.answer
        self.stop()

    @nextcord.ui.button(label="Audio", style = nextcord.ButtonStyle.blurple, disabled=False)
    async def audio_captcha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.audio_sent:
            answer = " ".join(letter for letter in self.actual_answer.split())
            bytes = io.BytesIO()
            tts = gTTS(answer)
            tts.save(bytes)
            bytes.seek(0)
            msg = await interaction.send(file=nextcord.File(bytes, f"{interaction.user}-audio.mp3"), ephemeral=True)
            self.audio_sent=True
        else:
            await interaction.send("You have already requested an audio captcha. Please use that to verify.", ephemeral=True)


    async def on_timeout(self):
        self.answer = "Too Long ---------------"
        self.stop()

class AnswerModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="What is your answer?")
        self.answer = nextcord.ui.TextInput(
            label = "What does the captcha say?",
            placeholder = "Example: qdvae",
            style=nextcord.TextInputStyle.short,
            min_length=1,
            max_length=10,
            required=True
        )
        self.add_item(self.answer)

    async def callback(self, interaction: nextcord.Interaction):
        self.answer = self.answer.value
        self.stop()