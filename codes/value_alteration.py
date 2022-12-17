# VALUE ALTERATION CODE V.1.1

# READ PLAN
table_reviews = PD.read_excel("sources/Teste.xlsx", sheet_name='2', dtype=str,
                                          keep_default_na=False)

line_count = len(table_reviews.index)
columns_count = len(table_reviews.columns)
reviews_list = []
for i in range(0, line_count):
    for j in range(0, columns_count):
        # INSERT LINE OF CRITICAL IN A LIST
        reviews_list.append(table_reviews.iloc[i][j])
        if len(reviews_list) == 4:  # WHEN LINE IS COMPLETE
            global guide_number, procedure_code, unitary_value, new_unitary_value
            [guide_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(
                reviews_list, 'values')

            reviews_list.clear()

            if guide_type == 'SADT':
                for account in guide_accounts:
                    if guide_number != '':
                        procedures_executed_and_expenses = getAllAccountProcedures(account)
                        specified_procedure_data = searchForSpecifiedProcedure(
                            procedures_executed_and_expenses['Executed procedures'],
                            procedures_executed_and_expenses['Expenses procedures'])

                        if specified_procedure_data is not None:
                            alterValue()
                            control_var += 1
                            break
                    else:
                        procedures_executed_and_expenses = getAllAccountProcedures(account)
                        specified_procedure_data = searchForSpecifiedProcedure(
                            procedures_executed_and_expenses['Executed procedures'],
                            procedures_executed_and_expenses['Expenses procedures'])
                        if specified_procedure_data is not None:
                            alterValue()
                            control_var += 1

            elif guide_type == 'HOSPITALIZATION':
                for account in guide_accounts:
                    procedures_executed_and_expenses = getAllAccountProcedures(account)
                    specified_procedure_data = searchForSpecifiedProcedure(
                        procedures_executed_and_expenses['Executed procedures'],
                        procedures_executed_and_expenses['Expenses procedures'])
                    if specified_procedure_data is not None:
                        alterValue()
                        control_var += 1