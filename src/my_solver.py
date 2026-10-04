import re
import argparse
import sys
from ArgumentationSystem import ArgumentationSystem

def parse_apx_file(filename):
    """
    Lit un fichier .apx et retourne un ArgumentationSystem
    """
    a_s = ArgumentationSystem()
    # Regex autorisant minuscules, majuscules, chiffres et underscores 
    arg_pattern = re.compile(r"arg\(([a-zA-Z0-9_]+)\)\.")
    att_pattern = re.compile(r"att\(([a-zA-Z0-9_]+),([a-zA-Z0-9_]+)\)\.")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                arg_match = arg_pattern.fullmatch(line)
                if arg_match:
                    a_s.add_argument(arg_match.group(1))
                    continue

                att_match = att_pattern.fullmatch(line)
                if att_match:
                    a, b = att_match.groups()
                    a_s.add_attack(a, b)
                    continue
                
                # Optionnel : lever une erreur si la ligne est malformée
                # raise ValueError(f"Ligne {line_num} invalide : {line}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        sys.exit(1)

    return a_s

def main():
    parser = argparse.ArgumentParser(description="Solveur de systèmes d'argumentation")

    # Gestion des drapeaux spécifiques du sujet  :
    # -P pour les problèmes de vérification (VE)
    # -p pour les problèmes de décision (DC, DS)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", dest="prob_decision", help="Problème DC ou DS")
    group.add_argument("-P", dest="prob_verif", help="Problème VE")

    parser.add_argument("-f", "--file", required=True, help="Fichier .apx")
    parser.add_argument("-a", "--args", required=True, help="Argument(s) de la requête")

    args = parser.parse_args()

    # Détermination du problème et vérification de la cohérence du drapeau
    if args.prob_verif:
        problem = args.prob_verif.upper()
        if not problem.startswith("VE"):
            # Le sujet demande -P pour VE [cite: 54-55]
            sys.exit(1)
    else:
        problem = args.prob_decision.upper()
        if not (problem.startswith("DC") or problem.startswith("DS")):
            # Le sujet demande -p pour DC/DS [cite: 58-60]
            sys.exit(1)

    # Chargement du système
    a_s = parse_apx_file(args.file)

    # Récupération brute des arguments (SANS .upper()) pour respecter la casse 
    arg_input_raw = args.args

    # --- Dispatcher ---

    # Cas VE-PR ou VE-ST (vérification d'ensemble)
    if problem in ["VE-PR", "VE-ST"]:
        # On sépare par virgule et on nettoie les espaces
        S = set(name.strip() for name in arg_input_raw.split(","))
        
        # Vérification d'existence des arguments dans le système
        if not S.issubset(a_s.arguments):
            print("NO")
            return

        if problem == "VE-PR":
            a_s.VE_PR(S)
        else:
            a_s.VE_ST(S)

    # Cas DC-XX ou DS-XX (décision sur un argument unique)
    elif problem in ["DC-PR", "DS-PR", "DC-ST", "DS-ST"]:
        target_arg = arg_input_raw.strip()

        if target_arg not in a_s.arguments:
            print("NO")
            return

        if problem == "DC-PR":
            a_s.DC_PR(target_arg)
        elif problem == "DS-PR":
            a_s.DS_PR(target_arg)
        elif problem == "DC-ST":
            a_s.DC_ST(target_arg)
        elif problem == "DS-ST":
            a_s.DS_ST(target_arg)

if __name__ == "__main__":
    main()