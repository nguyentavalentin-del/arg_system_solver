import sys
from itertools import combinations

class ArgumentationSystem:
    def __init__(self):
        self.arguments = set()
        self.attackers = dict()
        self.attacked_by = dict()

    def add_argument(self, arg):
        if arg not in self.arguments:
            self.arguments.add(arg)
            self.attackers[arg] = set()
            self.attacked_by[arg] = set()

    def add_attack(self, a, b):
        self.attacked_by[a].add(b)
        self.attackers[b].add(a)

    # --- LOGIQUE DE LABELLING (OPTIMISATION) ---

    def get_complete_labellings(self):
        """
        Trouve tous les étiquetages complets (légaux) par backtracking.
        C'est beaucoup plus rapide que de tester tous les sous-ensembles.
        """
        labellings = []
        args_list = list(self.arguments)
        
        def is_legal(arg, label, current_labelling):
            if label == 'in':
                # Tous les attaquants doivent être 'out'
                return all(current_labelling.get(atk) == 'out' for atk in self.attackers[arg])
            elif label == 'out':
                # Au moins un attaquant doit être 'in'
                return any(current_labelling.get(atk) == 'in' for atk in self.attackers[arg])
            elif label == 'undec':
                # Aucun attaquant n'est 'in' ET ils ne sont pas tous 'out'
                no_in = all(current_labelling.get(atk) != 'in' for atk in self.attackers[arg])
                not_all_out = any(current_labelling.get(atk) != 'out' for atk in self.attackers[arg])
                return no_in and not_all_out
            return False

        def backtrack(idx, current_labelling):
            if idx == len(args_list):
                # Vérification finale de la légalité pour tous les arguments
                # (nécessaire car un choix tardif peut invalider un choix précoce)
                for a in args_list:
                    lbl = current_labelling[a]
                    if lbl == 'in':
                        if not all(current_labelling.get(atk) == 'out' for atk in self.attackers[a]): return
                    elif lbl == 'out':
                        if not any(current_labelling.get(atk) == 'in' for atk in self.attackers[a]): return
                    elif lbl == 'undec':
                        no_in = all(current_labelling.get(atk) != 'in' for atk in self.attackers[a])
                        not_all_out = any(current_labelling.get(atk) != 'out' for atk in self.attackers[a])
                        if not (no_in and not_all_out): return
                labellings.append(current_labelling.copy())
                return

            arg = args_list[idx]
            for label in ['in', 'out', 'undec']:
                current_labelling[arg] = label
                backtrack(idx + 1, current_labelling)
                
        backtrack(0, {})
        return labellings

    # --- RÉPONSES AUX PROBLÈMES DU SUJET ---

    def get_preferred_extensions(self):
        # Une extension préférée est le 'in' d'un labelling complet maximal [cite: 1011]
        labs = self.get_complete_labellings()
        all_ins = [set(arg for arg, lbl in l.items() if lbl == 'in') for l in labs]
        preferred = []
        for s1 in all_ins:
            if not any(s1 < s2 for s2 in all_ins):
                if s1 not in preferred: preferred.append(s1)
        return preferred

    def get_stable_extensions(self):
        # Une extension stable est un labelling complet sans 'undec' [cite: 1021]
        labs = self.get_complete_labellings()
        stable = []
        for l in labs:
            if not any(lbl == 'undec' for lbl in l.values()):
                s = set(arg for arg, lbl in l.items() if lbl == 'in')
                if s not in stable: stable.append(s)
        return stable

    # --- COMMANDES CLI ---

    def VE_PR(self, S):
        print("YES" if S in self.get_preferred_extensions() else "NO")

    def DC_PR(self, a):
        print("YES" if any(a in s for s in self.get_preferred_extensions()) else "NO")

    def DS_PR(self, a):
        exts = self.get_preferred_extensions()
        print("YES" if exts and all(a in s for s in exts) else "NO")

    def VE_ST(self, S):
        print("YES" if S in self.get_stable_extensions() else "NO")

    def DC_ST(self, a):
        print("YES" if any(a in s for s in self.get_stable_extensions()) else "NO")

    def DS_ST(self, a):
        exts = self.get_stable_extensions()
        print("YES" if exts and all(a in s for s in exts) else "NO")