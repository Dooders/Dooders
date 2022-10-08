cube(`SimulationResults`, {
  sql: `SELECT * FROM public."SimulationResults"`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {},

  measures: {
    count: {
      type: `count`,
      drillMembers: [experimentid, cyclenumber],
    },

    doodercount: {
      sql: `${CUBE}."DooderCount"`,
      type: `sum`,
    },

    energycount: {
      sql: `${CUBE}."EnergyCount"`,
      type: `sum`,
    },

    totalenergysupply: {
      sql: `${CUBE}."TotalDooderEnergySupply"`,
      type: `sum`,
    },

    avgenergysupply: {
      sql: `${CUBE}."TotalDooderEnergySupply"`,
      type: `avg`,
    },

    energyage: {
      sql: `${CUBE}."AverageEnergyAge"`,
      type: `avg`,
    },
  },

  dimensions: {
    experimentid: {
      sql: `${CUBE}."ExperimentID"`,
      type: `string`,
    },

    cyclenumber: {
      sql: `${CUBE}."CycleNumber"`,
      type: `number`,
    },
  },

  dataSource: `default`,
});
