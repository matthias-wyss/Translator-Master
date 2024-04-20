# README - Translator Master Bot

Translator Master is a Telegram bot designed to facilitate language translation tasks seamlessly within the Telegram platform. This README provides essential information on how to set up and use the Translator Master bot effectively.

## Bot Access
You can access the Translator Master bot via Telegram by searching for `@test_translator_master_bot`.

## Installation
To get started with Translator Master, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by executing:
    ```
    pip install -r requirements.txt
    ```

## Usage
Once you have installed the necessary dependencies, you can launch the bot by running the `telegram_bot.py` script. This will activate the bot and enable its functionalities.

### Commands
Translator Master supports the following commands:

1. **text2text**:
   - Description: Translates a text input into the specified target language.
   - Usage: `/text2text [text] [target_language]`
   - Example: `/text2text Hello, how are you? fr_XX`

2. **text2speech**:
   - Description: Translates a text input into speech in the specified target language.
   - Usage: `/text2speech [text] [target_language]`
   - Example: `/text2speech Hello, how are you? fr_XX`

3. **speech2text**:
   - Description: Translates speech input into text in the specified target language.
   - Usage: `/speech2text [audio_file] [target_language]`
   - Example: `/speech2text [audio_file] fr_XX`

4. **speech2speech**:
   - Description: Translates speech input into speech in the specified target language.
   - Usage: `/speech2speech [audio_file] [target_language]`
   - Example: `/speech2speech [audio_file] fr_XX`

Note: Replace `[text]`, `[target_language]`, and `[audio_file]` with appropriate inputs.

## Languages Covered

Translator Master supports translation to and from the following languages:

- Arabic (ar_AR)
- Czech (cs_CZ)
- German (de_DE)
- English (en_XX)
- Spanish (es_XX)
- Estonian (et_EE)
- Finnish (fi_FI)
- French (fr_XX)
- Gujarati (gu_IN)
- Hindi (hi_IN)
- Italian (it_IT)
- Japanese (ja_XX)
- Kazakh (kk_KZ)
- Korean (ko_KR)
- Lithuanian (lt_LT)
- Latvian (lv_LV)
- Burmese (my_MM)
- Nepali (ne_NP)
- Dutch (nl_XX)
- Romanian (ro_RO)
- Russian (ru_RU)
- Sinhala (si_LK)
- Turkish (tr_TR)
- Vietnamese (vi_VN)
- Chinese (zh_CN)
- Afrikaans (af_ZA)
- Azerbaijani (az_AZ)
- Bengali (bn_IN)
- Persian (fa_IR)
- Hebrew (he_IL)
- Croatian (hr_HR)
- Indonesian (id_ID)
- Georgian (ka_GE)
- Khmer (km_KH)
- Macedonian (mk_MK)
- Malayalam (ml_IN)
- Mongolian (mn_MN)
- Marathi (mr_IN)
- Polish (pl_PL)
- Pashto (ps_AF)
- Portuguese (pt_XX)
- Swedish (sv_SE)
- Swahili (sw_KE)
- Tamil (ta_IN)
- Telugu (te_IN)
- Thai (th_TH)
- Tagalog (tl_XX)
- Ukrainian (uk_UA)
- Urdu (ur_PK)
- Xhosa (xh_ZA)
- Galician (gl_ES)
- Slovene (sl_SI)

Translator Master is capable of translating to and from these languages seamlessly, providing a comprehensive solution for multilingual communication needs.


## APIs Used
Translator Master utilizes the following APIs for its translation services:
- Hugging Face
- OpenAI

## Feedback and Support
For any feedback, suggestions, or issues encountered while using the Translator Master bot, please feel free to contact us. Your feedback is valuable for improving the bot's performance and user experience.

Thank you for using Translator Master!
