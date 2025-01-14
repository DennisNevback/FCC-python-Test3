import math

class Category:
    def __init__ (self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        display_final = ''
        #Constructing the header for display
        category_header_star = 30 - len(self.category)
        category_header_left = '*' * math.ceil((category_header_star / 2))
        #int auto rounds down
        category_header_right = '*' * int((category_header_star / 2))
        category_header_final = category_header_left + self.category + category_header_right + '\n'
        display_final += category_header_final

        #Constructing the summary
        category_summary = ''
        for i in self.ledger:
            #description
            category_description_length = 23 - len(i.get('description')[:23])
            category_description = i.get('description')[:23] + ' ' * category_description_length
            #amount
            amount_decimal_format = f"{i.get('amount'):.2f}"
            amount_description_length = 7 - len(amount_decimal_format[:7])
            amount_description = ' ' * amount_description_length + amount_decimal_format[:7]
            description_final = category_description + amount_description + '\n'
            display_final += description_final

        #Constructing the total
        total = 'Total: ' + str(self._get_balance())
        display_final += total

        return str(display_final)

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            amount = amount - (amount*2)
            self.ledger.append({'amount': amount, 'description': description})
            return True
        else:
            return False

    def _get_balance(self):
        balance = 0
        for i in self.ledger:
            balance += i.get('amount')
        return balance
    
    def get_balance(self):
        return self._get_balance()
    
    def transfer(self, amount, category):
        if self.withdraw(amount, (f"Transfer to {category.category}")):
            category.deposit(amount, (f"Transfer from {self.category}"))
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self._get_balance():
            return False
        else:
            return True


def _draw_spend_chart(category_percentages):
    #Print description
    final_string = 'Percentage spent by category\n'

    #Create rows
    rows = []
    for new_row in range(0,11):
        new_row *= 10
        rows.append([new_row])

    #find length of staple in diagram
    for i in category_percentages:
        bar_int_mulitplier = category_percentages.get(i)
        add_o = "o" * int(bar_int_mulitplier)
        for x in range(0,11):
            if x <= bar_int_mulitplier:
                rows[x].append('o')
            else:
                rows[x].append(' ')

    #Format Percentages and "o"
    for i in reversed(rows):
        formatted_string = ''
        for x in i:
            if (isinstance(x, int) and len(str(x)) == 1):
                formatted_string += '  ' + str(x) + '|' + ' '
            elif (isinstance(x, int) and len(str(x)) == 3):
                formatted_string += str(x) + '|' + ' '
            elif (isinstance(x, int) and len(str(x)) < 3 and len(str(x)) > 1):
                formatted_string += ' ' + str(x) + '|' + ' '
            else:
                formatted_string += '' + str(x) + '  '
        final_string += formatted_string + '\n'
    
    #print line using the last formatted string (The longest one)
    final_string += (' ' * 4 + '-' * (len(formatted_string) - 4))

    #Category name list
    category_name_list = [i for i in category_percentages]
    #Print category names
    category_name_string = ' '.join(category_name_list)
    #Split the string into words.
    words = category_name_string.split()
    #Find the length of the longest word to determine the number of rows.
    max_length = max(len(word) for word in words)

    # Create a list to hold the vertical print result.
    vertical_print = []

    # Iterate over the range of the maximum length found.
    for i in range(max_length):
        # Collect the i-th character of each word if it exists,
        # otherwise use a space.
        column_chars = [(word[i] + '  ' if i < len(word) else '   ') for word in words]

        # Join the characters to form the vertical word and
        # append it to the result list.
        vertical_print.append(''.join(column_chars))
    finished_string = '\n'

    for i in vertical_print:
        finished_string += ('     ' + i + '\n')
    final_string += finished_string

    # Return the final string and strip tailing \n

    final_string = final_string.rstrip('\n')
    print(final_string)
    return final_string

def _calculate_spend_percentages(categories):
    category_spending_list = {}
    total_spending = []
    for category in categories:
        total_spending += [i.get('amount') for i in category.ledger if i.get('amount') < 0]
    for category in categories:
        category_spending = [i.get('amount') for i in category.ledger if i.get('amount') < 0]
        category_percent_spending = math.trunc((sum(category_spending) / sum(total_spending)) * 10)
        category_spending_list[category.category] = category_percent_spending
    return category_spending_list

def create_spend_chart(categories):
    category_percentages = _calculate_spend_percentages(categories)
    spend_chart = _draw_spend_chart(category_percentages)
    return spend_chart


food = Category('food')
clothes = Category('Clothes')
other = Category('Other')
other.deposit(400, 'test')
other.withdraw(100, 'test')
other.withdraw(400, 'test')
clothes.deposit(800, 'vans')
food.deposit(900, 'deposit')
clothes.transfer(200, food)
food.withdraw(100, 'Bacon')
food.withdraw(200, 'Bacon')
clothes.withdraw(200, 'shirt')
#print(clothes)
#print(clothes.category)
#print(food.get_balance())
create_spend_chart([food, clothes, other])
