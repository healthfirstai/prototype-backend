
from healthfirstai_prototype.enums.openai_enums import ModelName

from healthfirstai_prototype.utils import get_model

llm = get_model(ModelName.gpt_3_5_turbo)
