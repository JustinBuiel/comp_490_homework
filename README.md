The production function is total_calculator in the tax_calculator.py file 

To run the tests use pytest via terminal or IDE GUI based testing

My project uses the pydantic version of python dataclasses for validation of fields so once a Product is instanciated (this is validated by _validate_cart) it is assumed to be good data

total_calculator as stated above does validation on its inputs; I was using pydantic.validate_arguments but didn't like the fact that it would convert things automatically since that is not good for readability in my oppinion; so now validation of types is done manually then validation of state abbbreviation is done. 