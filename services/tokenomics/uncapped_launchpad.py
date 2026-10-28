# Global Tokenomics & Uncapped-Mint Launchpad Engine
# Emission Function: M(t) = min(R(t), annual_emission_limit(t))
class UncappedTokenomicsEngine:
    def __init__(self, initial_supply=100_000_000, max_annual_inflation_bps=250):
        self.circulating_supply = initial_supply
        self.max_annual_inflation_bps = max_annual_inflation_bps # 2.50%
        self.total_burned = 0

    def calculate_allowable_mint(self, requested_mint_amount: int) -> int:
        max_annual_mint = (self.circulating_supply * self.max_annual_inflation_bps) // 10000
        approved_mint = min(requested_mint_amount, max_annual_mint)
        return approved_mint

    def execute_mint_and_burn(self, mint_amount: int, burn_amount: int):
        allowable = self.calculate_allowable_mint(mint_amount)
        self.circulating_supply += allowable
        self.circulating_supply -= burn_amount
        self.total_burned += burn_amount
        return {
            "minted": allowable,
            "burned": burn_amount,
            "circulating": self.circulating_supply,
            "burned_total": self.total_burned
        }
