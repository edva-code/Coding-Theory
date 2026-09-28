"""Terminal program for task A11: linear code C(n, k) with step-by-step decoding.

Run with:  python3 main.py
"""

import random

from coding import gf2
from coding.channel import BinarySymmetricChannel
from coding.decoder import StepByStepDecoder
from coding.linear_code import LinearCode, check_parameters, random_generator_matrix


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(ask(prompt))
        except ValueError:
            print("  Įveskite sveikąjį skaičių.")


def ask_probability(prompt: str) -> float:
    while True:
        try:
            pe = float(ask(prompt).replace(",", "."))
        except ValueError:
            print("  Įveskite skaičių, pvz. 0.1")
            continue
        if 0 <= pe <= 1:
            return pe
        print("  Tikimybė turi būti intervale [0, 1].")


def ask_vector(prompt: str, length: int, allow_empty: bool = False) -> gf2.Vector | None:
    while True:
        text = ask(prompt)
        if allow_empty and text == "":
            return None
        try:
            v = gf2.parse(text)
        except ValueError:
            print("  Vektorius turi būti sudarytas tik iš 0 ir 1.")
            continue
        if len(v) != length:
            print(f"  Vektoriaus ilgis turi būti {length}, o įvesta {len(v)}.")
            continue
        return v


def print_matrix(name: str, m: gf2.Matrix) -> None:
    print(f"{name} =")
    for row in m:
        print("   " + gf2.to_str(row))


def positions_1based(positions: list[int]) -> str:
    return ", ".join(str(i + 1) for i in positions) if positions else "-"


def setup_code(rng: random.Random) -> LinearCode:
    while True:
        n = ask_int("Kodo ilgis n: ")
        k = ask_int("Kodo dimensija k: ")
        try:
            check_parameters(n, k)
            break
        except ValueError:
            print("  Turi būti 0 < k < n.")

    while True:
        choice = ask("Generuojanti matrica G: [1] įvesti pačiam, [2] generuoti atsitiktinai: ")
        if choice == "2":
            return LinearCode(random_generator_matrix(n, k, rng))
        if choice == "1":
            print(f"Įveskite {k} eilutes po {n} bitų, standartinio pavidalo G = [I_{k} | A]:")
            rows = [ask_vector(f"  eilutė {i + 1}: ", n) for i in range(k)]
            try:
                return LinearCode(rows)
            except ValueError as error:
                print(f"  Netinkama matrica: {error}")


def show_decoding(decoder: StepByStepDecoder, received: gf2.Vector) -> gf2.Vector:
    s = decoder.syndrome_vector(received)
    print(f"Sindromas H·rᵀ = {gf2.to_str(s)}, klasės lyderio svoris w = {decoder.leader_weight(received)}")
    trace = []
    decoded = decoder.decode(received, trace)
    for step in trace:
        verdict = "apverčiam" if step.kept else "paliekam"
        print(f"  i={step.position + 1}: H(r+e_i)ᵀ = {gf2.to_str(step.new_syndrome)}, "
              f"svoris {step.new_weight} (buvo {step.old_weight}) -> {verdict}")
    return decoded


def scenario_vector(code: LinearCode, decoder: StepByStepDecoder,
                    channel: BinarySymmetricChannel) -> None:
    message = ask_vector(f"Pranešimas m (ilgis k={code.k}): ", code.k)
    codeword = code.encode(message)
    print(f"Užkoduotas vektorius c = m·G: {gf2.to_str(codeword)}")

    received, errors = channel.transmit(codeword)
    print(f"Iš kanalo gautas vektorius:   {gf2.to_str(received)}")
    print(f"Klaidų skaičius: {len(errors)}, pozicijos: {positions_1based(errors)}")

    edited = ask_vector("Redaguoti gautą vektorių (Enter - palikti kaip yra): ", code.n,
                        allow_empty=True)
    if edited is not None:
        received = edited
        diff = [i for i, bit in enumerate(gf2.add(codeword, received)) if bit]
        print(f"Dabar klaidų: {len(diff)}, pozicijos: {positions_1based(diff)}")

    decoded = show_decoding(decoder, received)
    decoded_message = code.extract_message(decoded)
    print(f"Dekoduotas kodo žodis:        {gf2.to_str(decoded)}")
    print(f"Dekoduotas pranešimas:        {gf2.to_str(decoded_message)}")
    if decoded_message == message:
        print("Pranešimas atkurtas teisingai.")
    else:
        print("Dekodavimas nepavyko: pranešimas skiriasi nuo išsiųsto.")


def main() -> None:
    rng = random.Random()  # created once and shared by G generation and the channel
    print("Tiesinis kodas C(n, k) ir dekodavimas žingsnis po žingsnio (A11)\n")
    code = setup_code(rng)
    decoder = StepByStepDecoder(code.H)
    print()
    print_matrix("G", code.G)
    print_matrix("H", code.H)
    channel = BinarySymmetricChannel(ask_probability("\nKlaidos tikimybė kanale pe: "), rng)

    while True:
        print(f"\n[1] siųsti vektorių   [2] keisti pe (dabar {channel.pe})   [0] baigti")
        choice = ask("> ")
        if choice == "1":
            scenario_vector(code, decoder, channel)
        elif choice == "2":
            channel.pe = ask_probability("Nauja pe: ")
        elif choice == "0":
            return


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
