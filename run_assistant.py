import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    # 1) загрузка .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    asst_id = os.getenv("ASSISTANT_ID")
    if not api_key or not asst_id:
        raise ValueError("Проверь .env: нужны OPENAI_API_KEY и ASSISTANT_ID")
    
    # 2) чтение промпта из файла
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            user_prompt = f.read().strip()
        print(f"Промпт загружен из prompt.txt: {user_prompt[:50]}...")
    except FileNotFoundError:
        raise ValueError("Файл prompt.txt не найден. Создайте файл с промптом.")
    except Exception as e:
        raise ValueError(f"Ошибка чтения prompt.txt: {e}")

    # 3) клиент
    client = OpenAI(api_key=api_key)

    # 4) получаем информацию об ассистенте для использования его настроек
    print("Получаем настройки ассистента...")
    assistant = client.beta.assistants.retrieve(assistant_id=asst_id)
    print(f"Ассистент: {assistant.name}")
    
    # 5) создаём запрос через новый Responses API с настройками ассистента
    print("Отправляем запрос ассистенту...")
    
    try:
        response = client.responses.create(
            model=assistant.model,  # Используем модель ассистента
            instructions=assistant.instructions,  # Используем системный промпт ассистента
            input=[
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ]
        )
        
        # 6) печатаем ответ ассистента
        print("\n--- Ответы ассистента ---")
        if hasattr(response, 'output') and response.output:
            for output in response.output:
                if hasattr(output, 'content') and output.content:
                    for content_block in output.content:
                        if hasattr(content_block, 'text'):
                            print(content_block.text)
            print("-" * 40)
        else:
            print("Ассистент не дал ответа")
            
        # 7) usage (если вернулся)
        if hasattr(response, 'usage') and response.usage:
            u = response.usage
            print(f"\nUsage: input_tokens={u.input_tokens}, output_tokens={u.output_tokens}, total_tokens={u.total_tokens}")
            
    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")
        raise

if __name__ == "__main__":
    main()
