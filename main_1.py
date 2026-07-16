from sarvamai import SarvamAI

client = SarvamAI(
    api_subscription_key="sk_6468jx6w_cuNGwZkI3iBTUSM1kqqq8nnY",
)

response = client.text.translate(
    input="Hi, My Name is Vinayak.",
    source_language_code="auto",
    target_language_code="gu-IN",
    speaker_gender="Male"
)

print(response)
