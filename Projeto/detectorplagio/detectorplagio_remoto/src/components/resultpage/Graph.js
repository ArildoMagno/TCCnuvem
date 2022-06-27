/*
eCharts examples -> https://ecomfe.github.io/echarts-examples/public/index.html
*/

import * as React from "react";
import {Component} from "react";
import ReactEcharts from "echarts-for-react";



const style_echarts = {
    height: "80vh",
    width: "100%",
};

export default class Graph extends Component {


    constructor(props) {
        super(props);

        this.state = {
            datafiles: props.datafiles,
        };
        this.manipulate_infos_graph = this.manipulate_infos_graph.bind(this);
    }


    //Chart options
    data_graph_links = []
    data_graph_file_names = []


    option = {
        responsive: false,

        series: [
            {
                name: 'Graph Result',
                type: "graph",
                layout: 'circular',
                symbolSize: 50,
                label: {
                    show: true,
                    formatter: '{b}'
                },


                data: this.data_graph_file_names,

                links: this.data_graph_links,

                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                },

                roam: true,

                emphasis: {
                    focus: 'adjacency',
                    lineStyle: {
                        width: 10
                    }
                }
            }
        ]
    };


    notContainsObject(obj, list) {
        var i;
        for (i = 0; i < list.length; i++) {
            if (list[i].name === obj.name) {
                return false;
            }
        }
        return true;
    }


    manipulate_infos_graph() {
        let data = this.state.datafiles


        for (let i = 0; i < data.length; i++) {
            let name_source = data[i].name_file_source
            name_source = name_source.substring(0, name_source.indexOf('.'));

            if (this.notContainsObject({name: name_source}, this.data_graph_file_names)) {
                this.data_graph_file_names.push({name: name_source});
            }

            for (let j = 0; j < data[i].relation_files.length; j++) {
                let relation_file = data[i].relation_files[j]
                let name_dest = relation_file.name_file_dest
                let similarity = relation_file.percent.toString()
                name_dest = name_dest.substring(0, name_dest.indexOf('.'));

                this.data_graph_links.push({
                    source: name_source,
                    target: name_dest,
                    label: {show: true, formatter: similarity}
                })
            }

        }

        this.data_graph_links = []
        this.data_graph_file_names = []

    }


    render() {
        this.manipulate_infos_graph()


        return (



                <ReactEcharts option={this.option} style={style_echarts}/>

        );
    }

}


