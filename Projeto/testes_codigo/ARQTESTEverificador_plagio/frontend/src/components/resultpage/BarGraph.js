import React, {PureComponent} from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

const data = [
  {
    name: "Page A",
    pv: 20,
  },
  {
    name: "Page B",
    pv: 30,
  },
  {
    name: "Page C",
    pv: 10,
  },
  {
    name: "Page D",
    pv: 40,
  },
  {
    name: "Page E",
    pv: 5,
  },
  {
    name: "Page F",
    pv: 12,
  },
  {
    name: "Page G",
    pv: 92,
  }
];

export default function BarGraph() {
  return (
    <BarChart
      width={500}
      height={300}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="pv" fill="#8884d8" />
    </BarChart>
  );
}
