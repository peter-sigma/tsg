from django import forms

VOICE_CHOICES = [
    ('edge_female', 'Edge TTS (Female - en-US-JennyNeural)'),
    ('edge_male', 'Edge TTS (Male - en-US-GuyNeural)'),
    ('gtts', 'Google TTS'),
    ('voicerss_linda', 'VoiceRSS (Linda - Female)'),
    ('voicerss_john', 'VoiceRSS (John - Male)'),
    ('voicerss_sarah', 'VoiceRSS (Sarah - Female)'),
    ('voicerss_mike', 'VoiceRSS (Mike - Male)'),
]

class TTSForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': 'Enter your text here'}),
        label="Text to Convert"
    )
    voice = forms.ChoiceField(choices=VOICE_CHOICES, label="Select Voice")