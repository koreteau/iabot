FROM deepseek-r1:14b

SYSTEM "Utilise les informations suivantes sur la Formule 1 pour répondre aux questions."

TEMPLATE "{{ .Prompt }}"

MESSAGE "{{ .Prompt }}"

INCLUDE data/calendrier/calendrier_f1_2020.md
INCLUDE data/calendrier/calendrier_f1_2021.md
INCLUDE data/calendrier/calendrier_f1_2022.md
INCLUDE data/calendrier/calendrier_f1_2023.md
INCLUDE data/calendrier/calendrier_f1_2024.md

INCLUDE data/classement/classement_f1_2020.md
INCLUDE data/classement/classement_f1_2021.md
INCLUDE data/classement/classement_f1_2022.md
INCLUDE data/classement/classement_f1_2023.md
INCLUDE data/classement/classement_f1_2024.md

INCLUDE data/constructeurs/constructeurs_f1_2020.md
INCLUDE data/constructeurs/constructeurs_f1_2021.md
INCLUDE data/constructeurs/constructeurs_f1_2022.md
INCLUDE data/constructeurs/constructeurs_f1_2023.md
INCLUDE data/constructeurs/constructeurs_f1_2024.md

INCLUDE data/circuits/circuits_f1_2020.md
INCLUDE data/circuits/circuits_f1_2021.md
INCLUDE data/circuits/circuits_f1_2022.md
INCLUDE data/circuits/circuits_f1_2023.md
INCLUDE data/circuits/circuits_f1_2024.md
