from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from transformers import MarianMTModel, MarianTokenizer
from rest_framework import status

# Function-based view for translation
@api_view(["POST"])
def translate_text(request):
    """
    API view that handles translation for a POST request with text, source language, and target language.
    """
    text = request.data.get("text", "")
    source_lang = request.data.get("source_lang", "en")
    target_lang = request.data.get("target_lang", "fr")

    if not text:
        return Response({"error": "No text provided for translation."}, status=status.HTTP_400_BAD_REQUEST)

    if not source_lang or not target_lang:
        return Response({"error": "Both source_lang and target_lang must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Load model and tokenizer based on language pair
        model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

        return Response({"translated_text": translated_text}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Translation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Class-based view for translation
class TranslationView(APIView):
    def post(self, request, *args, **kwargs):
        """
        API view that takes a POST request with text, source language, and target language,
        and returns the translated text.
        """
        text = request.data.get("text", "")
        source_lang = request.data.get("source_lang", "en")
        target_lang = request.data.get("target_lang", "fr")

        # Check if text is provided
        if not text:
            return Response({"error": "No text provided for translation."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate source and target languages
        if not source_lang or not target_lang:
            return Response({"error": "Both source_lang and target_lang must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Load model and tokenizer based on language pair
            model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)

            # Translate the text
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            translated = model.generate(**inputs)
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

            # Return the translated text as a response
            return Response({"translated_text": translated_text}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Translation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
