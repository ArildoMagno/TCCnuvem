import React, {Component} from "react";


export default class ResultPage extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div>
                <h1>Result Page:</h1>

                <div>
                    {this.props.location.state.map((documento, index) =>
                        <div key={index}>
                            <b>Nome Primeiro Arquivo:</b> {documento.name_file1} <br/>
                            <b>Nome Segundo Arquivo:</b> {documento.name_file2} <br/>

                            <h4>Sentenças:</h4>
                            {documento.similar_sets_log1.map((documento_inside, index_documento_inside) =>
                                <div key={index_documento_inside}>
                                    <b> Grau de semelhança entre Sentença Doc1 com Sentença
                                        Doc2</b>: {documento_inside.percentage_doc1_doc2} <br/>
                                    <b>Grau de semelhança entre Sentença Doc2 com Sentença
                                        Doc1: </b> {documento_inside.percentage_doc2_doc1} <br/>

                                    <b>Conteúdo Sentença Doc1: </b> {documento_inside.sentence_doc1} <br/>
                                    <b>Conteúdo Sentenca Doc2: </b> {documento_inside.sentence_doc2} <br/>
                                    <br/>
                                    <br/>
                                    <br/>
                                </div>
                            )}


                            <h3>Porcentagem Plagio Entre os Documentos:</h3> <h2> {documento.percent_plagiarism}</h2>
                            <br/>
                        </div>
                    )}
                </div>


            </div>
        );
    }
}


