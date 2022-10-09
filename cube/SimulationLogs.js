cube(`SimulationLogs`, {
  sql: `SELECT * FROM public."SimulationLogs"`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {},

  measures: {
    count: {
      type: `count`,
      drillMembers: [experimentId, id, timestamp],
    },
  },

  dimensions: {
    ExperimentID: {
      sql: `${CUBE}."ExperimentID"`,
      type: `string`,
    },

    CycleNumber: {
      sql: `${CUBE}."CycleNumber"`,
      type: `number`,
    },

    Scope: {
      sql: `${CUBE}."Scope"`,
      type: `string`,
    },

    ID: {
      sql: `${CUBE}."ID"`,
      type: `id`,
      primaryKey: true,
    },

    Message: {
      sql: `${CUBE}."Message"`,
      type: `string`,
    },

    Timestamp: {
      sql: `${CUBE}."Timestamp"`,
      type: `timestamp`,
    },
  },

  dataSource: `default`,
});
