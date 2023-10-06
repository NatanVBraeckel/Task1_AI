import re
import streamlit as st
from simpleai.search import CspProblem, backtrack


def solve_csp(inp):

    split_equal = inp.replace(' ', '').split("=")
    result = split_equal[-1]
    split_sign = split_equal[0].split("+")

    all_words = split_sign + [result]
    print(f'all_words = {all_words}')

    variables = set()
    domains = {}

    for word in all_words:
        for char in word:
            variables.add(char)
            if char == word[0]:
                domains[char] = list(range(1, 10))
            elif char not in domains:
                domains[char] = list(range(0, 10))

    variables = tuple(variables)

    print(f'\nvariables = {variables}')
    print(f'domains = {domains}')

    v = validate(all_words[:-1], all_words[-1])
    if isinstance(v, str):
        error.markdown(f':orange[{v}]')
        return

    def constraint_unique(variables, values):
        return len(values) == len(set(values))

    def constraint_add(variables, values):
        variable_value_map = dict(zip(variables, values))
        
        word_values = []
        for word in all_words:
            word_value = ''.join([str(variable_value_map[letter]) for letter in word])
            word_values.append(int(word_value))
        # word_values = [int(''.join([str(variable_value_map[letter]) for letter in word])) for word in all_words]
        
        return sum(word_values[:-1]) == word_values[-1]

    constraints = [
        (variables, constraint_unique),
        (variables, constraint_add)
    ]

    problem = CspProblem(variables, domains, constraints)

    output = backtrack(problem)

    if output:
        int_inp = inp
        for letter, value in output.items():
            int_inp = int_inp.replace(letter, str(value))
        st.subheader(f':blue[{inp}]', anchor=False)
        st.subheader(f':blue[{int_inp}]', anchor=False)
        st.markdown(f':gray[First solution found: {output}]')
    else:
        st.markdown(''':orange[No solutions found]''')


def validate(terms, result):    
    #terms and result moeten ingevuld zijn
    for term in terms:
        if not term:
            if not result: return "Terms and result can't be empty."
            return "Terms can't be empty."
        
    if not result: return "Result can't be empty." 

    #enkel letters als karakters
    for word in terms + [result]:
        pattern = r'^[A-Z]+$'
        if not re.match(pattern, word): return "Only use alphabetical characters." 

    #result moet de langste string zijn
    for term in terms:
        if len(term) > len(result):
            return "Terms can't be longer than result."

    #lengte van result can niet 2 langer zijn dan de langste term (bv: 99 + 99 =/= 1000)
    if max(len(term) for term in terms) < len(result) - 1: return "Result can't be 2 longer than the longest term."
    
    #niet meer dan totaal 10 karakters
    variables = set()
    for word in terms + [result]:
        for char in word:
            variables.add(char)
    if len(variables) > 10:
        return "You can only have a max of 10 different letters."


st.title(":red[Cryptarithmetic Solver] :mag_right:", anchor=False)

slidercol = st.columns(4)

with slidercol[0]:
    term_count = st.slider("Amount of terms", min_value=2, max_value=4)
    # term_count = st.selectbox('Aantal termen', (2, 3, 4))

cols = st.columns([.85,.15,.85,.15,.85,.15,.85,.15,.85,.15])

terms = []

for i in range(0, term_count * 2, 2):
    terms.append(cols[i].text_input(f"term", key=i, label_visibility="hidden"))

for i in range(1, term_count * 2, 2):
    cols[i].text("")
    cols[i].text("")
    if i == term_count * 2 - 1:
        cols[i].text("=")
    else:
        cols[i].text("+")

result = cols[term_count * 2].text_input("result", label_visibility="hidden")

error = st.empty()

if st.button('Solve'):
    terms_string = ' + '.join(terms).upper()
    inp = terms_string + f" = {result}".upper()
    solve_csp(inp)