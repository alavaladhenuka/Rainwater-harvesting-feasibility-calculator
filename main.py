"""
================================================================================
JNTUK B.TECH R23 REGULATION - SEMESTER 2 MINI-PROJECT
Project Title: Rainwater Harvesting Feasibility Calculator & Recommender
Domain Alignment: Civil Hydrodynamics (BCME) + Linear Algebra + CS Core
================================================================================

Course Outcomes (COs) Mapping:
--------------------------------------------------------------------------------
1. Civil Hydrodynamics: Rational Method Runoff Potential Assessment.
   Equation: H = A * R * C * E
   Where:
     H = Harvest Potential (Liters)
     A = Catchment Roof Area (m²)
     R = Annual Rainfall (mm)
     C = Runoff Coefficient (RCC/Sheet/Tile)
     E = System & First-Flush Efficiency Factor

2. Applied Mathematics (Linear Algebra):
   Multi-Sector Water Demand Matrix Allocation and Deficit Analysis.
   Formulation: [Demand Matrix] @ [Seasonal Multipliers] = [Net Demand Matrix]
   System Equations: [A][X] = [B] for Seasonal Deficit / Surplus Matrix

3. Computer Science / AI Integration:
   - Modular OOP Architecture
   - Robust Input Boundary Validation
   - AI Heuristic Recommendation Engine & System Prompt Generator
================================================================================
"""

import math
import sys

# Optional import with pure Python fallback for Matrix Operations
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# ==============================================================================
# 1. HYDRODYNAMICS FORMULA LIBRARY (CIVIL/MECH ENGINE)
# ==============================================================================
class HydrodynamicsEngine:
    """Implements Rational Method for rainwater runoff calculations."""

    # Roof Coefficients (C) based on standard engineering materials
    ROOF_COEFFICIENTS = {
        "1": ("Concrete / RCC Roof", 0.85),
        "2": ("Corrugated Metal Sheet", 0.90),
        "3": ("Clay / Ceramic Tile Roof", 0.75),
        "4": ("Asbestos Sheet", 0.80),
    }

    @staticmethod
    def calculate_annual_harvest(area: float, rainfall: float, coef: float, efficiency: float = 0.85) -> float:
        """
        Rational Method Formula:
        Volume (m³) = Area (m²) * Rainfall (m) * Runoff Coefficient * Efficiency
        Harvest (Liters) = Volume (m³) * 1000
        """
        rainfall_in_meters = rainfall / 1000.0
        harvest_m3 = area * rainfall_in_meters * coef * efficiency
        harvest_liters = harvest_m3 * 1000.0
        return harvest_liters

    @staticmethod
    def calculate_first_flush(area: float, intensity_mm: float = 1.0) -> float:
        """
        First-Flush Diverter Sizing:
        Rule of Thumb: Divert 1 Liter of water per m² of roof area for the first 1mm of rainfall.
        """
        return area * intensity_mm


# ==============================================================================
# 2. LINEAR ALGEBRA MATRIX ENGINE (APPLIED MATHEMATICS)
# ==============================================================================
class MatrixLinearAlgebraEngine:
    """
    Handles matrix operations for multi-sector household water demand,
    seasonal distribution, and surplus/deficit calculations.
    """

    # Per capita per day demand standards (Liters/person/day)
    PER_CAPITA_DEMAND = {
        "D1_Drinking_Cooking": 5.0,
        "D2_Flushing_Cleaning": 30.0,
        "D3_Gardening_Utility": 15.0,
    }

    def __init__(self, occupants: int):
        self.occupants = occupants

    # ✅ FIXED HERE: Added 'self' parameter to method definition
    def build_demand_matrix(self) -> list:
        """
        Constructs a 3x1 Daily Sector Demand Matrix [D] (Liters/day)
        D = [D1, D2, D3]^T
        """
        d1 = self.occupants * self.PER_CAPITA_DEMAND["D1_Drinking_Cooking"]
        d2 = self.occupants * self.PER_CAPITA_DEMAND["D2_Flushing_Cleaning"]
        d3 = self.occupants * self.PER_CAPITA_DEMAND["D3_Gardening_Utility"]
        return [[d1], [d2], [d3]]

    @staticmethod
    def multiply_matrices(a: list, b: list) -> list:
        """Pure Python Matrix Multiplication (Dot Product fallback if NumPy unavailable)."""
        if HAS_NUMPY:
            return np.matmul(np.array(a), np.array(b)).tolist()

        rows_a = len(a)
        cols_a = len(a[0])
        rows_b = len(b)
        cols_b = len(b[0])

        if cols_a != rows_b:
            raise ValueError("Matrix dimensions mismatch for multiplication.")

        result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def compute_seasonal_breakdown(self, annual_harvest: float) -> dict:
        """
        Solves seasonal supply vs demand balance using linear transformation.
        Monsoon Season (4 months = 120 days): 80% of rainfall
        Dry Season (8 months = 245 days): 20% of rainfall
        """
        demand_matrix = self.build_demand_matrix()  # 3x1 matrix
        daily_total_demand = sum(row[0] for row in demand_matrix)
        
        annual_total_demand = daily_total_demand * 365.0

        # Matrix [S] mapping seasonal proportions: [[Monsoon Supply], [Dry Supply]]
        seasonal_supply_matrix = [[0.80 * annual_harvest], [0.20 * annual_harvest]]

        # Seasonal Demand Vector (120 days monsoon, 245 days dry)
        seasonal_demand_matrix = [[daily_total_demand * 120.0], [daily_total_demand * 245.0]]

        # Compute Seasonal Surplus/Deficit: [Balance] = [Supply] - [Demand]
        monsoon_balance = seasonal_supply_matrix[0][0] - seasonal_demand_matrix[0][0]
        dry_balance = seasonal_supply_matrix[1][0] - seasonal_demand_matrix[1][0]

        return {
            "daily_demand_vector": demand_matrix,
            "daily_total_demand": daily_total_demand,
            "annual_total_demand": annual_total_demand,
            "monsoon_supply": seasonal_supply_matrix[0][0],
            "monsoon_demand": seasonal_demand_matrix[0][0],
            "monsoon_balance": monsoon_balance,
            "dry_supply": seasonal_supply_matrix[1][0],
            "dry_demand": seasonal_demand_matrix[1][0],
            "dry_balance": dry_balance,
            "annual_net_balance": annual_harvest - annual_total_demand,
        }


# ==============================================================================
# 3. AI / LLM RECOMMENDATION ENGINE LAYER
# ==============================================================================
class AIRecommender:
    """
    Simulates an LLM Reasoning Engine using rule-based heuristics & system prompt generation.
    Recommends tank dimensions, feasibility status, and engineering guidelines.
    """

    @staticmethod
    def evaluate_feasibility(annual_harvest: float, annual_demand: float, dry_balance: float) -> dict:
        coverage_ratio = (annual_harvest / annual_demand) * 100.0 if annual_demand > 0 else 0

        if coverage_ratio >= 100.0:
            verdict = "FULLY FEASIBLE"
            verdict_color = "GREEN"
            description = "Harvested water exceeds or fully meets the total annual household demand."
        elif coverage_ratio >= 40.0:
            verdict = "PARTIALLY FEASIBLE"
            verdict_color = "YELLOW"
            description = "Harvest meets primary non-potable needs. Dual-source integration recommended."
        else:
            verdict = "UNFEASIBLE / LOW POTENTIAL"
            verdict_color = "RED"
            description = "Roof catchment area or rainfall is insufficient for full-scale harvesting."

        daily_demand = annual_demand / 365.0
        optimal_tank_size = math.ceil((daily_demand * 45) / 500.0) * 500  # Rounded to nearest 500L

        return {
            "verdict": verdict,
            "verdict_color": verdict_color,
            "coverage_ratio": round(coverage_ratio, 2),
            "description": description,
            "recommended_tank_liters": optimal_tank_size,
        }

    @staticmethod
    def generate_llm_system_prompt(inputs: dict, results: dict) -> str:
        prompt = f"""
[SYSTEM PROMPT FOR HYDROLOGICAL AI ASSISTANT]
Task: Provide tailored civil engineering advice based on rainwater harvesting metrics.

INPUT DATA:
- Roof Catchment Area: {inputs['area']} m²
- Annual Rainfall: {inputs['rainfall']} mm
- Roof Material Coefficient: {inputs['coef']}
- Occupants: {inputs['occupants']}
- Annual Harvest Potential: {results['annual_harvest']:.2f} Liters
- Annual Household Water Demand: {results['annual_demand']:.2f} Liters
- Water Coverage Ratio: {results['coverage_ratio']}%
- Feasibility Verdict: {results['verdict']}

INSTRUCTIONS:
Generate 3 concrete recommendations for structural filtration, tank placement, and groundwater recharge.
"""
        return prompt.strip()


# ==============================================================================
# 4. CLI & INPUT VALIDATION INTERFACE
# ==============================================================================
class CLIInterface:
    """Handles User Input with boundary validation and formats the terminal output."""

    @staticmethod
    def print_header():
        print("=" * 80)
        print("    RAINWATER HARVESTING FEASIBILITY CALCULATOR & RECOMMENDER")
        print("    JNTUK B.Tech R23 Regulation - Applied Math & Hydrodynamics Mini-Project")
        print("=" * 80)

    @staticmethod
    def get_valid_float(prompt: str, min_val: float, max_val: float) -> float:
        while True:
            try:
                val = float(input(f"  > {prompt}: "))
                if min_val <= val <= max_val:
                    return val
                print(f"    [!] Value out of bounds. Must be between {min_val} and {max_val}.")
            except ValueError:
                print("    [!] Invalid input. Please enter a valid numerical value.")

    @staticmethod
    def get_valid_int(prompt: str, min_val: int, max_val: int) -> int:
        while True:
            try:
                val = int(input(f"  > {prompt}: "))
                if min_val <= val <= max_val:
                    return val
                print(f"    [!] Value out of bounds. Must be between {min_val} and {max_val}.")
            except ValueError:
                print("    [!] Invalid input. Please enter a valid integer.")

    @staticmethod
    def collect_inputs() -> dict:
        print("\n--- STEP 1: CATCHMENT & METEOROLOGICAL DATA INPUT ---")
        area = CLIInterface.get_valid_float("Enter Roof Catchment Area (in sq. meters, e.g., 100-500)", 10.0, 10000.0)
        rainfall = CLIInterface.get_valid_float("Enter Average Annual Rainfall (in mm, e.g., 800-2500)", 100.0, 10000.0)

        print("\n--- STEP 2: SELECT ROOF MATERIAL (Runoff Coefficient C) ---")
        for key, (mat_name, coef_val) in HydrodynamicsEngine.ROOF_COEFFICIENTS.items():
            print(f"    [{key}] {mat_name:<30} (C = {coef_val})")

        choice = ""
        while choice not in HydrodynamicsEngine.ROOF_COEFFICIENTS:
            choice = input("  > Select Roof Material Option (1-4): ").strip()
            if choice not in HydrodynamicsEngine.ROOF_COEFFICIENTS:
                print("    [!] Invalid choice. Please select 1, 2, 3, or 4.")

        mat_name, coef = HydrodynamicsEngine.ROOF_COEFFICIENTS[choice]

        print("\n--- STEP 3: HOUSEHOLD OCCUPANCY ---")
        occupants = CLIInterface.get_valid_int("Enter Number of Household Occupants", 1, 100)

        return {
            "area": area,
            "rainfall": rainfall,
            "coef_choice": choice,
            "mat_name": mat_name,
            "coef": coef,
            "occupants": occupants,
        }

    @staticmethod
    def display_results(inputs: dict, hydro_results: float, matrix_data: dict, ai_data: dict, first_flush: float):
        print("\n" + "=" * 80)
        print("                         PROJECT ANALYSIS DASHBOARD                     ")
        print("=" * 80)

        # 1. Hydrodynamics Summary
        print("\n[SECTION 1: HYDRODYNAMICS & RUNOFF EVALUATION (BCME)]")
        print("-" * 80)
        print(f"  * Roof Catchment Area      : {inputs['area']:.2f} m²")
        print(f"  * Annual Rainfall          : {inputs['rainfall']:.2f} mm")
        print(f"  * Roof Material            : {inputs['mat_name']} (C = {inputs['coef']})")
        print(f"  * Filter System Efficiency : 85.0%")
        print(f"  -> TOTAL ANNUAL HARVEST    : {hydro_results:,.2f} Liters ({hydro_results/1000:.2f} m³)")
        print(f"  -> FIRST-FLUSH VOLUME      : {first_flush:.2f} Liters (Required initial diversion)")

        # 2. Matrix Linear Algebra Breakdown
        print("\n[SECTION 2: LINEAR ALGEBRA DEMAND & SEASONAL MATRIX SOLVER]")
        print("-" * 80)
        print(f"  * Household Occupants      : {inputs['occupants']} Persons")
        print(f"  * Daily Sector Demand Vector [D] (L/day):")
        d_vec = matrix_data["daily_demand_vector"]
        print(f"    | D1 (Drinking/Cooking) | = {d_vec[0][0]:>7.2f} L/day")
        print(f"    | D2 (Flushing/Cleaning)| = {d_vec[1][0]:>7.2f} L/day")
        print(f"    | D3 (Gardening/Utility)| = {d_vec[2][0]:>7.2f} L/day")
        print(f"    ---------------------------------------")
        print(f"    TOTAL DAILY DEMAND       = {matrix_data['daily_total_demand']:>7.2f} L/day")
        print(f"    TOTAL ANNUAL DEMAND      = {matrix_data['annual_total_demand']:,.2f} L/year")

        print("\n  * Seasonal Balance Matrix [Supply - Demand]:")
        print(f"    Monsoon (4 Months) -> Supply: {matrix_data['monsoon_supply']:>10,.2f} L | Demand: {matrix_data['monsoon_demand']:>10,.2f} L | Net: {matrix_data['monsoon_balance']:>+10,.2f} L")
        print(f"    Dry Period (8 Months)-> Supply: {matrix_data['dry_supply']:>10,.2f} L | Demand: {matrix_data['dry_demand']:>10,.2f} L | Net: {matrix_data['dry_balance']:>+10,.2f} L")

        # 3. AI Recommender Layer
        print("\n[SECTION 3: AI / LLM FEASIBILITY & ENGINEERING RECOMMENDATIONS]")
        print("-" * 80)
        print(f"  * FEASIBILITY VERDICT      : [{ai_data['verdict']}]")
        print(f"  * Water Demand Coverage    : {ai_data['coverage_ratio']}% of total annual needs")
        print(f"  * Verdict Detail           : {ai_data['description']}")
        print(f"  * RECOMMENDED STORAGE TANK : {ai_data['recommended_tank_liters']:,} Liters")
        print(f"                               (Sized for ~45 Days Reserve Buffer)")

        print("\n[RECOMMENDED HYDRO-ENGINEERING ACTION PLAN]")
        print("  1. Installation: Position the first-flush diverter before the main filter.")
        print("  2. Maintenance: Inspect roof gutters pre-monsoon and clear debris.")
        if matrix_data['dry_balance'] < 0:
            print(f"  3. Supplementary Action: Dry season has a deficit of {abs(matrix_data['dry_balance']):,.2f} L.")
            print("     Implement dual piping to switch to municipal/borewell supply during dry months.")
        else:
            print("  3. Surplus Action: Underground recharge pit recommended for excess monsoon overflow.")

        print("=" * 80 + "\n")


# ==============================================================================
# MAIN EXECUTION PIPELINE
# ==============================================================================
def main():
    CLIInterface.print_header()

    # Step 1: Input Collection
    user_inputs = CLIInterface.collect_inputs()

    # Step 2: Hydrodynamics Calculation
    annual_harvest = HydrodynamicsEngine.calculate_annual_harvest(
        area=user_inputs["area"],
        rainfall=user_inputs["rainfall"],
        coef=user_inputs["coef"],
        efficiency=0.85,
    )
    first_flush_vol = HydrodynamicsEngine.calculate_first_flush(area=user_inputs["area"])

    # Step 3: Matrix Linear Algebra Calculation
    matrix_engine = MatrixLinearAlgebraEngine(occupants=user_inputs["occupants"])
    seasonal_data = matrix_engine.compute_seasonal_breakdown(annual_harvest=annual_harvest)

    # Step 4: AI Recommender Evaluation
    ai_evaluation = AIRecommender.evaluate_feasibility(
        annual_harvest=annual_harvest,
        annual_demand=seasonal_data["annual_total_demand"],
        dry_balance=seasonal_data["dry_balance"],
    )

    # Step 5: Dashboard Output Generation
    CLIInterface.display_results(
        inputs=user_inputs,
        hydro_results=annual_harvest,
        matrix_data=seasonal_data,
        ai_data=ai_evaluation,
        first_flush=first_flush_vol,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    [!] Execution cancelled by user. Exiting gracefully.")
        sys.exit(0)