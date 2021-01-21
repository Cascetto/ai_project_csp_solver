# CSP solver
### Richiede python 3.9
Risolve csp a vincoli binari generici
Per usare:
- instanziare un CSP()
- aggiungere variabili con il metodo CSP.add_variable(varname: str, domains: list[str])
--- è possibile specificare un range di valori, usando la sintassi di minizinc ('first..last')
- aggiungere i vincoli con CSP.add_constraint(cons: str)
--- la valutazione del vincolo è effettuata usando la funzione eval() di python, quindi il vincolo di ugualianza è '=='
- invocare backtrack(csp, inference_strategy)
--- inference_stratecy può essere: no_inference, forward_checking, maintaint_arc_consistency (tutti funcion objects)

nb: per creare problemi di nqueen s sudoku sono fornite le funzioni create_n_*(size: int)
    è fornita anche una funzione per stampare i risultati: print_*(size: int, solution: dict)
