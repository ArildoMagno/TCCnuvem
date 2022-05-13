import React, {Component} from "react";

export default class DetailsResult extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div>
                <h1>Detalhes:</h1>

                {this.props.location.state.map((document, index) => (
                    <div key={index}>
                        <b>Documento:</b> {document.name_file_dest}
                        <b>Similaridade das sentenças em relação ao documento origina e este:</b>


                        1-Arrumar esse MAP aqui, deve ser só mapear a saída
                        2-Procurar um Layout para essa página de detalhes e deixar ela mais bonita

                        {document.similar_set_source_dest.map((document_inside, index_inside) => (
                            <div key={index_inside}>{document_inside}</div>
                        ))}


                    </div>
                ))}

            </div>
        );
    }
}

