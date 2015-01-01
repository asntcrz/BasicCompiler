# -*- coding: utf-8 -*-
###******************************************************************************
### COMPILADORES 2009-2010****IMPLEMENTACION DE LA TABLA DE DECISION DEL LL(1) **
###******************************************************************************
###
###******************************************************************************


def td_crearTablaDec():
   global tablaDecision
   tablaDecision = {
    '_S':{ 'EOL':['_S_Acc()','S','Pop1_Acc()'],                     # _S -> {acc} S
            'def':['_S_Acc()','S','Pop1_Acc()'],                    # _S -> {acc} S
            'dim':['_S_Acc()','S','Pop1_Acc()'],                    # _S -> {acc} S
            'if':['_S_Acc()','S','Pop1_Acc()'],                     # _S -> {acc} S
            'input':['_S_Acc()','S','Pop1_Acc()'],                  # _S -> {acc} S
            'let':['_S_Acc()','S','Pop1_Acc()'],                    # _S -> {acc} S
            'print':['_S_Acc()','S','Pop1_Acc()'],                  # _S -> {acc} S
            'while':['_S_Acc()','S','Pop1_Acc()']},                 # _S -> {acc} S
    'S':{ 'EOL':['EOL','S','S_Acc1()','Pop2_Acc()'],                # S -> EOL S {acc1}
            'def':['D_Def','S','S_Acc2()','Pop2_Acc()'],            # S -> D_Def S {acc2}
            'dim':['D_Dim','S','S_Acc3()','Pop2_Acc()'],            # S -> D_Dim S {acc3}
            'if':['S_Acc4()','Sent','S1','S_Acc5()','Pop2_Acc()'],             # S -> {acc4} Sent S1 {acc5}
            'input':['S_Acc4()','Sent','S1','S_Acc5()','Pop2_Acc()'],          # S -> {acc4} Sent S1 {acc5}
            'let':['S_Acc4()','Sent','S1','S_Acc5()','Pop2_Acc()'],            # S -> {acc4} Sent S1 {acc5}
            'print':['S_Acc4()','Sent','S1','S_Acc5()','Pop2_Acc()'],          # S -> {acc4} Sent S1 {acc5}
            'while':['S_Acc4()','Sent','S1','S_Acc5()','Pop2_Acc()']},         # S -> {acc4} Sent S1 {acc5}
    'S1':{'EOL':['EOL','S1','S1_Acc1()','Pop2_Acc()'],             # S1 -> EOL S1 {acc1}
            'end':['end','S2','S1_Acc2()','Pop2_Acc()'],           # S1 -> end S2 {acc2}
            'if':['Sent','S1','S1_Acc3()','Pop2_Acc()'],           # S1 -> Sent S1 {acc3}
            'input':['Sent','S1','S1_Acc4()','Pop2_Acc()'],        # S1 -> Sent S1 {acc4}
            'let':['Sent','S1','S1_Acc5()','Pop2_Acc()'],          # S1 -> Sent S1 {acc5}
            'print':['Sent','S1','S1_Acc6()','Pop2_Acc()'],        # S1 -> Sent S1 {acc6}
            'while':['Sent','S1','S1_Acc7()','Pop2_Acc()']},       # S1 -> Sent S1 {acc7}
    'S2':{'$':['/','S2_Acc0()'],                                   # S2 -> / {acc0}
          'EOL':['EOL','S2','S2_Acc1()','Pop2_Acc()']},            # S2 -> EOL S2 {acc0}
    'D_Def':{'def':['def','id','D_Def_Acc()','T','Pop3_Acc()']},                # D_Def -> def id {acc} T
    'T':{'(':['(','Arg',')','EOL','BD','end','def','T_Acc()','Pop7_Acc()'],     # T -> ( Arg ) EOL BD end def {acc}
        'EOL':['EOL','BD','end','def','T_Acc()','Pop4_Acc()']},                 # T -> EOL BD end def {acc}
    'Arg':{'id':['id','Y','Arg_Acc1()','W','Arg_Acc2()','Pop3_Acc()']},         # Arg -> id Y {acc1} W {acc2}
    'Y':{',':['/','Y_Acc1()'],                           # Y -> / {acc1}
         ')':['/','Y_Acc1()'],                           # Y -> / {acc1}
         '(':['(','int',')','Y_Acc2()','Pop3_Acc()']},   # Y -> ( int ) {acc2}
    'W':{')':['/','W_Acc1()'],                           # W -> / {acc1}
         ',':[',','Arg','W_Acc2()','Pop2_Acc()']},       # W -> , Arg {acc2}
    'BD':{'dim':['D_Dim','BodyDef','BD_Acc1()','Pop2_Acc()'],        # BD -> D_Dim BodyDef {acc1}
          'static':['D_Static','BodyDef','BD_Acc3()','Pop2_Acc()'],  # BD -> D_Static BodyDef {acc3}
          'if':['Sent', 'BodyDef','BD_Acc2()','Pop2_Acc()'],         # BD -> Sent BodyDef {acc2}
          'input':['Sent','BodyDef','BD_Acc2()','Pop2_Acc()'],       # BD -> Sent BodyDef {acc2}
          'let':['Sent','BodyDef','BD_Acc2()','Pop2_Acc()'],         # BD -> Sent BodyDef {acc2}
          'print':['Sent','BodyDef','BD_Acc2()','Pop2_Acc()'],       # BD -> Sent BodyDef {acc2}
          'while':['Sent','BodyDef','BD_Acc2()','Pop2_Acc()']},      # BD -> Sent BodyDef {acc2}
   'BodyDef':{'dim':['BD','BodyDef_Acc1()','Pop1_Acc()'],       # BodyDef -> BD {acc1}
              'end':['/','BodyDef_Acc2()'],                     # BodyDef -> / {acc2}
              'if':['BD','BodyDef_Acc1()','Pop1_Acc()'],        # BodyDef -> BD {acc1}
              'input':['BD','BodyDef_Acc1()','Pop1_Acc()'],     # BodyDef -> BD {acc1}
              'let':['BD','BodyDef_Acc1()','Pop1_Acc()'],       # BodyDef -> BD {acc1}
              'print':['BD','BodyDef_Acc1()','Pop1_Acc()'],     # BodyDef -> BD {acc1}
              'static':['BD','BodyDef_Acc1()','Pop1_Acc()'],    # BodyDef -> BD {acc1}
              'while':['BD','BodyDef_Acc1()','Pop1_Acc()'],     # BodyDef -> BD {acc1}
              'EOL':['EOL','Pop1_Acc()']},                      # BodyDef -> EOL
    'D_Dim':{'dim':['dim','id','(','int',')','D_Dim_Acc()','Q','Pop6_Acc()']},   # D_Dim -> dim id ( int ) {acc} Q                           
    'Q':{',':[',','id','(','int',')','Q_Acc()','Q','Pop6_Acc()'],                    # Q -> , id ( int ) {acc} Q
         'EOL':['EOL','Pop1_Acc()']},                                            # Q -> EOL
    'D_Static':{'static':['static','id','D_Static_Acc()','A','Pop3_Acc()']},     # D_Static -> static id {acc1} A
    'A':{',': [',','id','A_Acc()','A','Pop3_Acc()'],	    # A ->, id {acc1} A
               'EOL': ['EOL','Pop1_Acc()'] },			    # A -> EOL        
    'Sent':{'if':['Sent_If','EOL','Sent_Acc1()', 'Pop2_Acc()'],        # Sent -> Sent_If EOL {acc1}
            'input':['Sent_IO','EOL','Sent_Acc2()','Pop2_Acc()'],      # Sent -> Sent_IO EOL {acc2}
            'print':['Sent_IO','EOL','Sent_Acc2()','Pop2_Acc()'],      # Sent -> Sent_IO EOL {acc2}
            'let':['Sent_Let','EOL','Sent_Acc3()','Pop2_Acc()'],       # Sent -> Sent_Let EOL {acc3}
            'while':['Sent_While','EOL','Sent_Acc4()','Pop2_Acc()']},  # Sent -> Sent_While EOL {acc4}
    'Sent_If':{'if':['if','Exp','Sent_If_Acc1()','then','X','Sent_If_Acc2()','Pop4_Acc()']},        # Sent_if -> if Exp {acc1}then X {acc2}
    'X':{'input':['Sent_IO','X_Acc1()','Pop1_Acc()'],                          # X -> Sent_IO {acc1}
         'print':['Sent_IO','X_Acc1()','Pop1_Acc()'],                           # X -> Sent_IO {acc1}
         'let':['Sent_Let','X_Acc2()','Pop1_Acc()']},                             # X -> Sent_Let {acc2}
    'Sent_IO':{ 'input':['Sent_Input','Sent_IO_Acc1()','Pop1_Acc()'],            # Sent_IO -> Sent_Input {acc1}
                'print':['Sent_Print','Sent_IO_Acc2()','Pop1_Acc()']},           # Sent_IO -> Sent_Print {acc2}
    'Sent_Input':{'input':['input','id','Sent_Input_Acc0()','Z','Sent_Input_Acc1()','Pop3_Acc()']},   # Sent_Input -> input id {acc0} Z {acc1}
    'Z':{'EOL':['/','Z_Acc1()'],                                                 # Z -> / {acc1}
        '(':['(','Exp',')','Z_Acc2()','Pop3_Acc()']},                            # Z -> ( Exp ) {acc2}
    'Sent_Print':{'print':['print','P','Sent_Print_Acc()','Pop2_Acc()']},        # Sent_Print -> print P {acc}
    'P':{'(':['Exp','R','P_Acc()','Pop2_Acc()'],                     # P -> Exp R {acc}
         '-':['Exp','R','P_Acc()','Pop2_Acc()'],                     # P -> Exp R {acc}
         'cadena':['Exp','R','P_Acc()','Pop2_Acc()'],                # P -> Exp R {acc}
         'id':['Exp','R','P_Acc()','Pop2_Acc()'],                    # P -> Exp R {acc}
         'int':['Exp','R','P_Acc()','Pop2_Acc()']},                  # P -> Exp R {acc}
   'R':{';':[';','P','R_Acc2()','Pop2_Acc()'],                      # R -> ; P {acc2}
        'EOL':['/', 'R_Acc1()']},                                   # R -> / {acc1}  
   'Sent_Let':{'let':['let','id','Sent_Let_Acc0()','M','Sent_Let_Acc1()','=','Exp','Sent_Let_Acc2()','Pop5_Acc()']}, # Sent_Let -> let id {acc0} M {acc1} = Exp {acc2}
   'M':{'(':['(','Exp',')','M_Acc1()','Pop3_Acc()'],                            # M -> ( Exp ) {acc1}
        '=':['/','M_Acc2()']},                                                  # M -> / {acc2}
   'Sent_While':{'while':['while','Sent_While_Acc1()','Exp','Sent_While_Acc2()',
                          'EOL','Sent','Sent_Gen', 'Sent_While_Acc3()', 'wend','Pop6_Acc()']}, # Sent_While -> while {acc1} Exp {acc2} EOL Sent  Sent_Gen {acc3} wend
    'Sent_Gen':{'if':['Sent','Sent_Gen','Sent_Gen_Acc1()','Pop2_Acc()'],         # Sent_Gen -> Sent Sent_Gen {acc1}
                'input':['Sent','Sent_Gen','Sent_Gen_Acc1()','Pop2_Acc()'],      # Sent_Gen -> Sent Sent_Gen {acc1}
                'let':['Sent','Sent_Gen','Sent_Gen_Acc1()','Pop2_Acc()'],        # Sent_Gen -> Sent Sent_Gen {acc1}
                'print':['Sent','Sent_Gen','Sent_Gen_Acc1()','Pop2_Acc()'],      # Sent_Gen -> Sent Sent_Gen {acc1}
                'while':['Sent','Sent_Gen','Sent_Gen_Acc1()','Pop2_Acc()'],     # Sent_Gen -> Sent Sent_Gen {acc1}
                'wend':['/','Sent_Gen_Acc2()']},                                  # Sent_Gen -> / {acc2}
                
   'Exp':{'(':['AA','Exp_Acc1()','_Exp','Exp_Acc2()','Pop1_Acc()'],     # Exp -> AA {acc1(con pop)} _Exp {acc2}
          '-':['AA','Exp_Acc1()','_Exp','Exp_Acc2()','Pop1_Acc()'],     # Exp -> AA {acc1(con pop)} _Exp {acc2}
          'id':['AA','Exp_Acc1()','_Exp','Exp_Acc2()','Pop1_Acc()'],    # Exp -> AA {acc1(con pop)} _Exp {acc2}
          'int':['AA','Exp_Acc1()','_Exp','Exp_Acc2()','Pop1_Acc()'],	# Exp -> AA {acc1(con pop)} _Exp {acc2}
         'cadena':['AA','Exp_Acc1()','_Exp','Exp_Acc2()','Pop1_Acc()']},# Exp -> AA {acc1(con pop)} _Exp {acc2}
   'AA':{'(':['BB','AA_Acc1()','_AA','AA_Acc2()','Pop1_Acc()'],		    # AA -> BB {acc1(con pop)} _AA {acc2}
        '-':['BB','AA_Acc1()','_AA','AA_Acc2()','Pop1_Acc()'],          # AA -> BB {acc1(con pop)} _AA {acc2}
        'id':['BB','AA_Acc1()','_AA','AA_Acc2()','Pop1_Acc()'],		    # AA -> BB {acc1(con pop)} _AA {acc2}
        'int':['BB','AA_Acc1()','_AA','AA_Acc2()','Pop1_Acc()'],		# AA -> BB {acc1(con pop)} _AA {acc2}
        'cadena':['BB','AA_Acc1()','_AA','AA_Acc2()','Pop1_Acc()']},    # AA -> BB {acc1(con pop)} _AA {acc2}        
   'BB':{'(':['CC','BB_Acc1()','_BB','BB_Acc2()','Pop1_Acc()'],         # BB -> CC {acc1(con pop)} _BB {acc2}
        '-':['CC','BB_Acc1()','_BB','BB_Acc2()','Pop1_Acc()'],          # BB -> CC {acc1(con pop)} _BB {acc2}
        'id':['CC','BB_Acc1()','_BB','BB_Acc2()','Pop1_Acc()'],		    # BB -> CC {acc1(con pop)} _BB {acc2}
        'int':['CC','BB_Acc1()','_BB','BB_Acc2()','Pop1_Acc()'],		# BB -> CC {acc1(con pop)} _BB {acc2}
        'cadena':['CC','BB_Acc1()','_BB','BB_Acc2()','Pop1_Acc()']},    # BB -> CC {acc1(con pop)} _BB {acc2}        
   'CC':{'(':['DD','CC_Acc1()','_CC','CC_Acc2()','Pop1_Acc()'],         # CC -> DD {acc1(con pop)} _CC {acc2}
          '-':['DD','CC_Acc1()','_CC','CC_Acc2()','Pop1_Acc()'],        # CC -> DD {acc1(con pop)} _CC {acc2}
          'id':['DD','CC_Acc1()','_CC','CC_Acc2()','Pop1_Acc()'],       # CC -> DD {acc1(con pop)} _CC {acc2}
          'int':['DD','CC_Acc1()','_CC','CC_Acc2()','Pop1_Acc()'],	    # CC -> DD {acc1(con pop)} _CC {acc2}
         'cadena':['DD','CC_Acc1()','_CC','CC_Acc2()','Pop1_Acc()']},   # CC -> DD {acc1(con pop)} _CC {acc2}         
   'DD':{'(':['EE','DD_Acc1()','_DD','DD_Acc2()','Pop1_Acc()'],		    # DD -> EE {acc1(con pop)} _DD {acc2}
        '-':['EE','DD_Acc1()','_DD','DD_Acc2()','Pop1_Acc()'],          # DD -> EE {acc1(con pop)} _DD {acc2}
        'id':['EE','DD_Acc1()','_DD','DD_Acc2()','Pop1_Acc()'],		    # DD -> EE {acc1(con pop)} _DD {acc2}
        'int':['EE','DD_Acc1()','_DD','DD_Acc2()','Pop1_Acc()'],		# DD -> EE {acc1(con pop)} _DD {acc2}
        'cadena':['EE','DD_Acc1()','_DD','DD_Acc2()','Pop1_Acc()']},    # DD -> EE {acc1(con pop)} _DD {acc2}        
   'EE':{'(':['FF','EE_Acc1()','_EE','EE_Acc2()','Pop1_Acc()'],         # EE -> FF {acc1(con pop)} _EE {acc2}
        '-':['FF','EE_Acc1()','_EE','EE_Acc2()','Pop1_Acc()'],          # EE -> FF {acc1(con pop)} _EE {acc2}
        'id':['FF','EE_Acc1()','_EE','EE_Acc2()','Pop1_Acc()'],		    # EE -> FF {acc1(con pop)} _EE {acc2}
        'int':['FF','EE_Acc1()','_EE','EE_Acc2()','Pop1_Acc()'],		# EE -> FF {acc1(con pop)} _EE {acc2}
        'cadena':['FF','EE_Acc1()','_EE','EE_Acc2()','Pop1_Acc()']},    # EE -> FF {acc1(con pop)} _EE {acc2}         
   'FF':{'(':['GG','FF_Acc1()','_FF','FF_Acc2()','Pop1_Acc()'],		    # FF -> GG {acc1(con pop)} _FF {acc2}
        '-':['GG','FF_Acc1()','_FF','FF_Acc2()','Pop1_Acc()'],          # FF -> GG {acc1(con pop)} _FF {acc2}
        'id':['GG','FF_Acc1()','_FF','FF_Acc2()','Pop1_Acc()'],		    # FF -> GG {acc1(con pop)} _FF {acc2}
        'int':['GG','FF_Acc1()','_FF','FF_Acc2()','Pop1_Acc()'],		# FF -> GG {acc1(con pop)} _FF {acc2}
        'cadena':['GG','FF_Acc1()','_FF','FF_Acc2()','Pop1_Acc()']},    # FF -> GG {acc1(con pop)} _FF {acc2}        
   'GG':{'(':['U','GG_Acc1()','_GG','GG_Acc2()','Pop1_Acc()'],          # GG -> U  {acc1(con pop)} _GG {acc2}
        '-':['U','GG_Acc1()','_GG','GG_Acc2()','Pop1_Acc()'],           # GG -> U  {acc1(con pop)} _GG {acc2}
        'id':['U','GG_Acc1()','_GG','GG_Acc2()','Pop1_Acc()'],		    # GG -> U  {acc1(con pop)} _GG {acc2}
        'int':['U','GG_Acc1()','_GG','GG_Acc2()','Pop1_Acc()'],		    # GG -> U  {acc1(con pop)} _GG {acc2}
        'cadena':['U','GG_Acc1()','_GG','GG_Acc2()','Pop1_Acc()']},     # GG -> U  {acc1(con pop)} _GG {acc2}
   'U':{'(':['H','U_Acc1()','Pop1_Acc()'],              # U -> H {acc1}
        'cadena':['H','U_Acc1()','Pop1_Acc()'],         # U -> H {acc1}
        'id':['H','U_Acc1()','Pop1_Acc()'],             # U -> H {acc1}
        'int':['H','U_Acc1()','Pop1_Acc()'],            # U -> H {acc1}
        '-':['-','H','U_Acc2()','Pop2_Acc()']},         # U -> - H {acc2}                                         
   'H':{'(':['(','Exp',')','H_Acc0()','Pop3_Acc()'],    # H -> ( Exp ) {acc0}
        'id':['id','H_Acc1()','I','H_Acc2()','Pop2_Acc()'],# H -> id {acc1} I {acc2}
        'int':['int','H_Acc3()','Pop1_Acc()'],          # H -> int {acc3}
        'cadena':['cadena','H_Acc4()','Pop1_Acc()']},	# H -> cadena {acc4}
   'I':{'(':['(','J',')','I_Acc1()','Pop3_Acc()'],		# I -> ( J ) {acc1}
        ')':['/','I_Acc2()'],                           # I -> / {acc2}
        'or':['/','I_Acc2()'],                          # I -> / {acc2}
        'and':['/','I_Acc2()'],                         # I -> / {acc2}
        '<>':['/','I_Acc2()'],                          # I -> / {acc2}
        '>':['/','I_Acc2()'],                           # I -> / {acc2}
        '<':['/','I_Acc2()'],                           # I -> / {acc2}
        '=':['/','I_Acc2()'],                           # I -> / {acc2}
        '+':['/','I_Acc2()'],                           # I -> / {acc2}
        '-':['/','I_Acc2()'],                           # I -> / {acc2}
        ',':['/','I_Acc2()'],                           # I -> / {acc2}
        ';':['/','I_Acc2()'],                           # I -> / {acc2}
        'EOL':['/','I_Acc2()'],                         # I -> / {acc2}
        'then':['/','I_Acc2()']},                       # I -> / {acc2}
   'J':{'(':['Exp','K','J_Acc()','Pop2_Acc()'],	        # J -> Exp K {acc} 
        '-':['Exp','K','J_Acc()','Pop2_Acc()'],         # J -> Exp K {acc} 
        'id':['Exp','K','J_Acc()','Pop2_Acc()'],	    # J -> Exp K {acc} 
        'int':['Exp','K','J_Acc()','Pop2_Acc()'],      # J -> Exp K {acc} 
        'cadena':['Exp','K','J_Acc()','Pop2_Acc()']},    # J -> Exp K {acc} 
   'K':{')':['/','K_Acc1()'],			                        # K -> / {acc1}
        ',':[',','J','K_Acc2()','Pop2_Acc()']},		            # K -> , J {acc2}
   '_Exp':{')':['/','_Exp_Acc0()'],                     # _Exp -> / {acc0}
           ',':['/','_Exp_Acc0()'],                     # _Exp -> / {acc0}
           ';':['/','_Exp_Acc0()'],                     # _Exp -> / {acc0}
           'EOL':['/','_Exp_Acc0()'],		            # _Exp -> / {acc0}
           'then':['/','_Exp_Acc0()'],		            # _Exp -> / {acc0}
           'or':['or','AA','_Exp_Acc1()','_Exp']},      # _Exp -> or AA {acc1} _Exp
   '_AA':{')':['/','_AA_Acc0()'],			            # _AA -> / {acc0}
         ',':['/','_AA_Acc0()'],			            # _AA -> / {acc0}			
         ';':['/','_AA_Acc0()'],			            # _AA -> / {acc0}
         'or':['/','_AA_Acc0()'],		                # _AA -> / {acc0}
         'EOL':['/','_AA_Acc0()'],		                # _AA -> / {acc0}
         'then':['/','_AA_Acc0()'],		                # _AA -> / {acc0}
         'and':['and','BB','_AA_Acc1()','_AA']},        # _AA -> and BB {acc1} _AA
   '_BB':{')':['/','_BB_Acc0()'],			            # _BB -> / {acc0}
         ',':['/','_BB_Acc0()'],			            # _BB -> / {acc0}
         ';':['/','_BB_Acc0()'],			            # _BB -> / {acc0}
         'or':['/','_BB_Acc0()'],		                # _BB -> / {acc0}		
         'and':['/','_BB_Acc0()'],		                # _BB -> / {acc0}	
         'EOL':['/','_BB_Acc0()'],		                # _BB -> / {acc0}
         'then':['/','_BB_Acc0()'],		                # _BB -> / {acc0}
         '<>':['<>','CC','_BB_Acc1()','_BB']},          # _BB -> <> CC {acc1} _BB
   '_CC':{')':['/','_CC_Acc0()'],			            # _CC -> / {acc0}
         ',':['/','_CC_Acc0()'],			            # _CC -> / {acc0}			
         ';':['/','_CC_Acc0()'],			            # _CC -> / {acc0}
         'or':['/','_CC_Acc0()'],		                # _CC -> / {acc0}
         'and':['/','_CC_Acc0()'],		                # _CC -> / {acc0}
         '<>':['/','_CC_Acc0()'],		                # _CC -> / {acc0}
         'EOL':['/','_CC_Acc0()'],		                # _CC -> / {acc0}
         'then':['/','_CC_Acc0()'],		                # _CC -> / {acc0}
         '=':['=','DD','_CC_Acc1()','_CC']},            # _CC -> = DD {acc1} _CC
   '_DD':{')':['/','_DD_Acc0()'],			            # _DD -> / {acc0}
         ',':['/','_DD_Acc0()'],			            # _DD -> / {acc0}
         ';':['/','_DD_Acc0()'],			            # _DD -> / {acc0}
         'or':['/','_DD_Acc0()'],		                # _DD -> / {acc0}		
         'and':['/','_DD_Acc0()'],		                # _DD -> / {acc0}
         '<>':['/','_DD_Acc0()'],		                # _DD -> / {acc0}
         '=':['/','_DD_Acc0()'],		                # _DD -> / {acc0}		
         'EOL':['/','_DD_Acc0()'],		                # _DD -> / {acc0}
         'then':['/','_DD_Acc0()'],		                # _DD -> / {acc0}
         '<':['<','EE','_DD_Acc1()','_DD']},            # _DD -> < EE {acc1} _DD     
   '_EE':{')':['/','_EE_Acc0()'],			            # _EE -> / {acc0}
         ',':['/','_EE_Acc0()'],			            # _EE -> / {acc0}
         ';':['/','_EE_Acc0()'],			            # _EE -> / {acc0}
         'or':['/','_EE_Acc0()'],		                # _EE -> / {acc0}		
         'and':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         '<>':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         '=':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         '<':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         'EOL':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         'then':['/','_EE_Acc0()'],		                # _EE -> / {acc0}
         '>':['>','FF','_EE_Acc1()','_EE']},            # _EE -> > FF {acc1} _EE     
   '_FF':{')':['/','_FF_Acc0()'],			            # _FF -> / {acc0}
         ',':['/','_FF_Acc0()'],			            # _FF -> / {acc0}			
         ';':['/','_FF_Acc0()'],			            # _FF -> / {acc0}
         'or':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         'and':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         '<>':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         '=':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         '<':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         '>':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         'EOL':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         'then':['/','_FF_Acc0()'],		                # _FF -> / {acc0}
         '-':['-','GG','_FF_Acc1()','_FF']},            # _FF -> - GG {acc1} _FF
   '_GG':{')':['/','_GG_Acc0()'],			            # _GG -> / {acc0}
         ',':['/','_GG_Acc0()'],			            # _GG -> / {acc0}
         ';':['/','_GG_Acc0()'],			            # _GG -> / {acc0}
         'or':['/','_GG_Acc0()'],		                # _GG -> / {acc0}		
         'and':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '<>':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '=':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '<':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '>':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '-':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         'EOL':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         'then':['/','_GG_Acc0()'],		                # _GG -> / {acc0}
         '+':['+','U','_GG_Acc1()','_GG']}}            # _GG -> + U {acc1} _GG
         
         
def td_consultarTablaDec (clave, valor):
    global tablaDecision
    if tablaDecision.has_key(clave):
       listaaux = tablaDecision[clave]
       if listaaux.has_key(valor):
          lista = listaaux.get(valor)
          return lista
       else:
          return []
    else:
       return []

def generar_TD():
   global tablaDecision
   return (str(tablaDecision))
