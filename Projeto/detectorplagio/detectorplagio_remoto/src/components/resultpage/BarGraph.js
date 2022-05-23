import React, {Component} from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";

let data = [];

export default class BarGraph extends Component {

    constructor(props) {
        super(props);

        this.state = {
            datafiles: props.datafiles,
        };
        this.manipulate_infos_graph = this.manipulate_infos_graph.bind(this);
    }

    manipulate_infos_graph() {
        data = []
        let file_infos = this.state.datafiles
        for (let i = 0; i < file_infos.length; i++) {
            let file_data =
                {
                    name: file_infos[i].name_file_dest,
                    porcentagem: file_infos[i].percent,
                }
            data.push(file_data)
        }
    }


    render() {

        this.manipulate_infos_graph()

        return (
            <BarChart
                width={400}
                height={400}
                data={data}
                margin={{
                    top: 5,
                    right: 40,
                    left: 20,
                    bottom: 5
                }}
            >
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="name"/>
                <YAxis type="number" domain={[0, 100]}/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="porcentagem" fill="#92A8D1"/>
            </BarChart>
        );
    }
}