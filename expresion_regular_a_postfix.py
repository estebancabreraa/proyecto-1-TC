def regular_a_postfix(expression_check):
    stack = []    
    symbols_to_insert = ['+', '-', 'x', '(', '|']
    not_allow = ['(']
        
    final_result = ""                    
    for c in expression_check:      
        
        if c == ')':
            for s in range(len(stack)):
                s_temp = stack.pop()
                if s_temp not in not_allow:
                    final_result += s_temp 
                    
        elif c in symbols_to_insert:
            stack.append(c)
            
        else:
            final_result += c
            
    for s in range(len(stack)):
        final_result += stack.pop()
        
    return final_result
