ASSETS = {
    "🌳 Urban Park": {
        "cost": 2_500_000, "water_cost": 400, "upkeep_cost": 450_000, "upkeep_water":100,
        "heat_mod": 0.6, "solar_mod": 0, "income": 0,
        "env_mod": 5, "biz_mod": -2, "res_mod": 3,
        "desc_cost": "Cost: $2.5M | Water: 400 Units",
        "desc_upkeep": "Upkeep: $450K/yr | Water Use: 100/yr",
        "desc_effect": "Effect: -0.6°C Heat | +5 Env, -2 Biz, +3 Res Approval"
    },
    "☀️ Solar Array": {
        "cost": 5_000_000, "water_cost": 0, "upkeep_cost": 200_000, "upkeep_water": 0,
        "heat_mod": 0.0, "solar_mod": 1200, "income": 600_000,
        "env_mod": 4, "biz_mod": -2, "res_mod": 2,
        "desc_cost": "Cost: $5.0M | Water: 0 Units",
        "desc_upkeep": "Upkeep: $800K/yr | Clean Energy: 1,200 kWh/yr",
        "desc_effect": "Effect: +$600K/yr | +4 Env, -2 Biz, +2 Res Approval"
    },
    "💧 Eco Reservoir": {
        "cost": 7_500_000, "water_cost": 0, "upkeep_cost": 800_000, "upkeep_water":-1_500,
        "heat_mod": 0.2, "solar_mod": 0, "income": 0,
        "env_mod": 2, "biz_mod": -1, "res_mod": 6,
        "desc_cost": "Cost: $7.5M | Water: 0 Units",
        "desc_upkeep": "Upkeep: $800K/yr",
        "desc_effect": "Effect: +1,500 Water/yr | +2 Env, -1 Biz, +6 Res Approval"
    },
    "🏭 Industrial Factory": {
        "cost": 4_000_000, "water_cost": 600, "upkeep_cost": 500_000, "upkeep_water": 400,
        "heat_mod": -0.8, "solar_mod": 0, "income": 3_200_000,
        "env_mod": -8, "biz_mod": 7, "res_mod": -4,
        "desc_cost": "Cost: $4.0M | Water: 600 Units",
        "desc_upkeep": "Upkeep: $500K/yr | Water: 400/yr",
        "desc_effect": "Effect: +$3.2M/yr, +0.8°C Heat | -8 Env, +7 Biz, -4 Res Approval"
    },
    "🏢 Commercial Block": {
        "cost":6_000_000, "water_cost": 800, "upkeep_cost": 700_000, "upkeep_water": 300,
        "heat_mod": -0.4, "solar_mod": 0, "income": 2_100_000,
        "env_mod": -4, "biz_mod": 5, "res_mod": -2,
        "desc_cost": "Cost: $6.0M | Water: 800 Units",
        "desc_upkeep": "Upkeep: $700K/yr | Water: 300/yr",
        "desc_effect": "Effect: +2.1M/yr, +0.4°C Heat | -4 Env, +5 Biz, -2 Res Approval"
    }
}

goals = [
    {"name": "Fiscal Conservative", "desc": "Have >20M net worth at end of term"},
    {"name": "Water Security", "desc": "Have water reserves of at least 2,000 at end of term"},
    {"name": "Pro-Growth Administration", "desc": "Maximize business approval to 80% by end of term"},
    {"name": "Climate Activist", "desc": "Achieve 2.0°C heat island reduction by end of term"},
    {"name": "Population Peacemaker", "desc": "End with approvals of all groups >70%"}
]