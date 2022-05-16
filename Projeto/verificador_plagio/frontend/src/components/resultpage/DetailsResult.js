import React, {Component} from "react";

export default class DetailsResult extends Component {
    constructor(props) {
        super(props);
        console.log("ENTRADA:", this.props.location.state)
    }


    render() {
        return (
            <div>
                <h1>Detalhes:</h1>

                {this.props.location.state.sentences.map((document, index) => (
                    <div key={index}>

                        <br/> <br/><br/> <b>Similaridade das sentenças em relação aos
                        documentos {this.props.location.state.document_name} e {document.name_file_dest} :</b>


                        {document.similar_set_dest_source.map((document_inside, index_inside) => (
                            <div key={index_inside}>
                                <b>Sentença {index_inside}</b>
                                <br/><b>Documento {document.name_file_dest}: </b>{document_inside.sentence_doc1}
                                <br/><b>Documento {this.props.location.state.document_name}: </b>{document_inside.sentence_doc2}

                            </div>
                        ))}


                    </div>
                ))}

            </div>
        );
    }
}

