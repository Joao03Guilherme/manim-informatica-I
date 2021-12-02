from manim import *

class binary_list(Scene):
    def construct(self):
        """
        INICIAL TEXT
        """
        text1 = MarkupText(f"Afterschool <span fgcolor='{BLUE}'>Informática I</span>").scale(1.2)
        self.play(FadeIn(text1))
        self.wait(2)

        text2 = MarkupText(f"Explicação do exercício <span fgcolor='{BLUE}'>8</span> da semana <span fgcolor='{RED}'>4</span>").scale(0.6).next_to(text1, DOWN)
        self.play(FadeIn(text2))
        self.wait(2)

        v = VGroup(text1, text2)
        self.play(FadeOut(v))
        # INICIAL SCREEN ENDED

        """
        SECRET KEY IS A BINARY LIST
        """
        text1 = MarkupText(f"A chave secreta é uma lista <span fgcolor='{BLUE}'>binária</span>").scale(0.8).to_edge(UP)
        self.play(FadeIn(text1))
        self.wait(2)

        # Create tables
        row1, row2 = ["1", "0", "0", "0", "1", "1"], ["0", "0", "0", "0", "0", "0"]
        t1 = Table([row1], include_outer_lines=True).scale(0.6) # SECRET KEY
        t2 = Table([row1], include_outer_lines=True).scale(0.6) # CURRENT KEY
        row_obj = t2.get_rows()[0] 
        # Add text to secret key
        text2 = Text("Chave secreta", gradient=(BLUE, GREEN)).scale(0.5).next_to(t1, LEFT)

        # Render tables and text
        self.play(Create(t1)) # Secret key table
        self.play(FadeIn(text2)) # Secret key text
        self.add(t2) # Current key (in background)
        
        self.wait(2)

        # Move secret key down
        v = VGroup(t1, text2)
        self.play(v.animate.shift(1.5*DOWN), run_time=2)        

        # Transform current key to all zeroes
        self.play(FadeOut(text1)) # Remove previous text
        textn = Text("A primeira tentativa contém apenas zeros").scale(0.8).to_edge(UP)
        self.play(FadeIn(textn))
        self.wait(2)

        tentativa = ValueTracker(0) 
        text3 = always_redraw(lambda: Text(f"Tentativa = {int(tentativa.get_value())}", gradient=(BLUE, GREEN)).scale(0.5).next_to(t2,LEFT))
        self.play(FadeIn(text3))
        self.play(Transform(t2, Table([row2], include_outer_lines=True).scale(0.6)), run_time = 1) # Transform table to all zeroes
        self.wait(2)

        self.play(FadeOut(textn))
        # BINARY LIST SCENE ENDED

        """
        CALCULATE NUMBER OF INCORRECT DIGITS
        :currently_shown: t1, t2, text2, text3
        """
        incorretos = ValueTracker(-1)
        minincorretos = ValueTracker(-1)

        text4 = MarkupText(f"<span fgcolor='{BLUE}'>Incorretos</span> - Número de incorretos da tentativa atual").scale(0.6).to_edge(UP)
        text5 = MarkupText(f"<span fgcolor='{BLUE}'>Mínimo Incorretos</span> - Número mínimo de incorretos já encontrado").scale(0.6).next_to(text4, DOWN)
        text6 = always_redraw(lambda: MarkupText(f"Mínimo incorretos = <span fgcolor='{BLUE}'>{'?' if minincorretos.get_value() == -1 else int(minincorretos.get_value())}</span>").scale(0.6).next_to(text5, DOWN, buff=0.4))
        text7 = always_redraw(lambda: MarkupText(f"Incorretos = <span fgcolor='{BLUE}'>{'?' if incorretos.get_value() == -1 else int(incorretos.get_value())}</span>").scale(0.6).next_to(text6, DOWN, buff=0.4))
        
        v = VGroup(text4, text5)
        self.play(FadeIn(v))
        self.wait(3)
        
        v = VGroup(text6, text7)
        self.play(FadeIn(v))
        self.wait(2)

        # Calculate number of incorrect digits
        incorretos += 1 
        minincorretos += 1
        self.wait(1)

        def incorrect_count(t1, r1, r2, incorretos):
            """
            :param: t1: secret key table (down table)
                    r1: secret key array
                    r2: current key array
                    incorretos: reference to value tracker
            """
            incorretos.set_value(0) 
            self.wait(0.5)

            row_obj = t1.get_rows()[0] # List with submobject objects
            prev_vec = Vector(UP).next_to(row_obj[0], DOWN, buff=0.6).scale(0.8) 
            self.play(FadeIn(prev_vec))

            # Loop in the table
            for i in range(len(r1)):
                curr_vec = Vector(UP).next_to(row_obj[i], DOWN, buff=0.6).scale(0.8)
                self.play(ReplacementTransform(prev_vec, curr_vec)) # Update prev vector
                self.wait(0.2)

                if r1[i] != r2[i]:
                    incorretos += 1

                self.wait(0.2)
                prev_vec = curr_vec

            self.wait(1)
            self.play(FadeOut(prev_vec))

        # Inicial counting
        vec = Vector(UP, color=BLUE).next_to(row_obj[0], DOWN, buff=0.6).scale(0.8)
        self.play(FadeIn(vec))
        incorrect_count(t1, row1, row2, incorretos)
        self.play(FadeOut(vec))
        
        # Update minimum value
        minincorretos.set_value(int(incorretos.get_value()))
        self.wait(1)

        # Fade out screen
        v = VGroup(t1, t2, text4, text5, text6, text7, text2, text3)
        self.play(FadeOut(v))
        # CALCULATE NUMBER OF INCORRECT DIGITS SCENE ENDED

        """
        PSEUDOCODE
        """
        text8 = MarkupText(f"<span fgcolor='{RED}'>Pseudocódigo</span>").scale(0.8).to_edge(UP)
        self.play(FadeIn(text8))
        self.wait(1)

        code = '''Alteramos o dígito da tentativa atual
Se o número de incorretos agora é menor:
    Atualizamos o número mínimo de incorretos
    Mantemos a alteração do dígito anterior
Senão:
    Revertemos a alteração do dígito anterior'''
        rendered_code = Code(code=code, tab_width=4, background="window",
                            language="pypy", font="Monospace", color=BLUE)
        self.play(FadeIn(rendered_code))
        self.wait(14)

        # Clear scene
        v1 = VGroup(text8, rendered_code)
        self.play(FadeOut(v1))
        # PSEUDOCODE SCENE ENDED

        """
        ALGORITHM REPRESENTATION
        :currently_shown: t1, t2, text2, text3, text4, text5, text6, text7, 
        """

        # Show tables
        v = VGroup(t1, t2, text2, text3, text6, text7)
        self.play(FadeIn(v)) 

        text9 = MarkupText(f"<span fgcolor='{RED}'>Execução</span> do programa").scale(0.8).to_edge(UP)
        self.play(FadeIn(text9))
        self.wait(1)

        def transform_table(t2, r2, i):
            row_obj = t2.get_rows()[0]
            self.play(Transform(row_obj[i], Paragraph(r2[i]).move_to(row_obj[i].get_center()).scale(0.6)))

        # t1 -> Secret key, t2 -> Current key
        def update_minimum(incorretos, minincorretos, title_text, t2):
            row_obj = t2.get_rows()[0]
            if incorretos.get_value() < minincorretos.get_value():
                minincorretos.set_value(incorretos.get_value())
                text = Text("2. O número de incorretos diminuiu, mantemos o dígito").scale(0.5).next_to(title_text, DOWN)
                self.play(FadeIn(text))
            else:
                text = Text("2. O número de incorretos não diminuiu, voltamos a alterar o dígito").scale(0.5).next_to(title_text, DOWN)
                self.play(FadeIn(text))
                self.wait(1)

                prev_t = int(tentativa.get_value() - 1)
                row2[prev_t] = "0" if row2[prev_t] == "1" else "1" # Revert old value
                transform_table(t2, row2, prev_t)

            self.wait(2)
            self.play(FadeOut(text))

        for i in range(6):
            # Add current vector
            vec = Vector(UP, color=BLUE).next_to(row_obj[i], DOWN, buff=0.6).scale(0.8)
            self.play(FadeIn(vec))

            # First step
            # Count number of incorrect digits
            incorrect_count(t1, row1, row2, incorretos)

            # Second step
            text10 = Text("1. Alterar número atual").scale(0.5).next_to(text9, DOWN)
            self.play(FadeIn(text10))

            # Flip current digit
            if row2[i] == "0": row2[i] = "1" 
            else: row2[i] = "0"
            transform_table(t2, row2, i)
            self.wait(2)

            self.play(FadeOut(text10))

            # First try
            if i == 0:
                text11 = Text("2. Na primeira tentativa não há nada a comparar, seguimos").scale(0.5).next_to(text9, DOWN)
                self.play(FadeIn(text11))
                self.wait(2)
                self.play(FadeOut(text11))
                tentativa += 1
                continue

            # Third step
            update_minimum(incorretos, minincorretos, text9, t2)

            if i != 5:
                self.play(FadeOut(vec))
                tentativa += 1
        
        # Last pass
        incorrect_count(t1, row1, row2, incorretos, 5)
        # ALGORITHM SCENE ENDED

        """
        NUMBER OF INCORRECT DIGITS IS 0 - PROGRAM HAS ENDED
        """
        self.wait(1)
        text12 = MarkupText(f"O número de incorretos é <span fgcolor='{BLUE}'>0</span>, a execução do programa <span fgcolor='{RED}'>terminou</span>").scale(0.6).next_to(text9, DOWN)
        self.play(FadeIn(text12))
        self.wait(3)

        # FadeOut scene
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)

        # Initial text
        text13 = MarkupText(f"Afterschool <span fgcolor='{BLUE}'>Informática I</span>").scale(1.2)
        self.play(FadeIn(text13))
        self.wait(4)
