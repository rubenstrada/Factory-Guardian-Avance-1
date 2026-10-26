"""Interfaz de terminal; no guarda conversaciones ni modifica conocimiento."""
import argparse

from .bot import FactoryGuardianBot


def main():
    parser = argparse.ArgumentParser(description="Factory Guardian: consultas con datos ficticios")
    parser.add_argument("--text", help="Una consulta completa; sin este argumento abre el diálogo de terminal.")
    args = parser.parse_args()
    bot = FactoryGuardianBot()
    if args.text is not None:
        reply = bot.respond(args.text)
        print(f"[{reply.intent}] {reply.text}")
        return
    print("Factory Guardian | datos ficticios | escribe 'salir' para terminar.")
    while True:
        try:
            text = input("Tú: ")
        except (EOFError, KeyboardInterrupt):
            print("\nFin de la sesión.")
            break
        reply = bot.respond(text)
        print(f"Bot [{reply.intent}]: {reply.text}")
        if text.strip().casefold() == "salir":
            break


if __name__ == "__main__":
    main()
