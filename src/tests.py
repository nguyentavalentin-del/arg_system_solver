from ArgumentationSystem import ArgumentationSystem

def run_test(name, expected, func, *args):
    """Utilitaire pour afficher le résultat d'un test"""
    print(f"Test {name} :", end=" ")
    # On capture la sortie standard car tes méthodes font des print()
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    func(*args)
    sys.stdout = sys.__stdout__
    result = captured_output.getvalue().strip()
    
    if result == expected:
        print(f"✅ RÉUSSI (Reçu: {result})")
    else:
        print(f"❌ ÉCHEC (Attendu: {expected}, Reçu: {result})")

if __name__ == "__main__":
    # --- CONFIGURATION DU SYSTÈME (FIGURE 1 DU SUJET) ---
    # AF = <{a,b,c,d}, {(a,b), (b,c), (b,d)}> 
    a_s = ArgumentationSystem()
    for arg in ["a", "b", "c", "d"]:
        a_s.add_argument(arg)

    a_s.add_attack("a", "b") # a attaque b [cite: 1268]
    a_s.add_attack("b", "c") # b attaque c [cite: 1269]
    a_s.add_attack("b", "d") # b attaque d [cite: 1270]

    print("=== TESTS OFFICIELS (FIGURE 1) ===")

    # 1. Vérification d'extension Préférée (VE-PR) [cite: 1294-1297]
    run_test("VE-PR {a,c,d}", "YES", a_s.VE_PR, {"a", "c", "d"})
    run_test("VE-PR {a}", "NO", a_s.VE_PR, {"a"})

    # 2. Acceptabilité Sceptique Préférée (DS-PR) [cite: 1298]
    # 'a' est dans toutes les extensions préférées car il n'est pas attaqué
    run_test("DS-PR 'a'", "YES", a_s.DS_PR, "a")

    # 3. Acceptabilité Crédule Préférée (DC-PR) [cite: 1299]
    # 'b' est attaqué par 'a' qui est accepté, donc 'b' est toujours rejeté
    run_test("DC-PR 'b'", "NO", a_s.DC_PR, "b")

    print("\n=== TESTS SÉMANTIQUE STABLE (ST) ===")

    # 4. Vérification d'extension Stable (VE-ST)
    # {a,c,d} attaque tout ce qui est à l'extérieur (b), donc c'est stable [cite: 1240]
    run_test("VE-ST {a,c,d}", "YES", a_s.VE_ST, {"a", "c", "d"})
    
    # 5. Acceptabilité Crédule Stable (DC-ST)
    run_test("DC-ST 'c'", "YES", a_s.DC_ST, "c")

    print("\n=== TESTS DE PERFORMANCE (CAS COMPLEXES) ===")
    
    # Test d'un cycle de 3 (Paradoxe : pas d'extension stable) [cite: 1618, 2054]
    paradox = ArgumentationSystem()
    for arg in ["a1", "a2", "a3"]: paradox.add_argument(arg)
    paradox.add_attack("a1", "a2")
    paradox.add_attack("a2", "a3")
    paradox.add_attack("a3", "a1")
    
    run_test("Paradoxe VE-ST {a1}", "NO", paradox.VE_ST, {"a1"})
    # Sous ST, un cycle impair n'a aucune extension, donc DS doit être NO 
    run_test("Paradoxe DS-ST 'a1'", "NO", paradox.DS_ST, "a1")