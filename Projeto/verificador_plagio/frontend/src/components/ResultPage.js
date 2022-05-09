import React, {Component} from "react";


export default class ResultPage extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div>
                <h2>Result Page:</h2>
                {/*Por la passo objeto e aqui itero/mapeio ele para ter acesso*/}
                <div>
                    {this.props.location.state.map((item, index) =>
                        <div key={index}>
                            <h4>Resultado: {index}</h4>
                            <b>Nome Primeiro Arquivo:</b> {item.name_file1} <br/>
                            <b>Nome Segundo Arquivo:</b> {item.name_file2} <br/>
                            <b>Nome Conjuntos Similares Primeiro Arquivo:</b> {item.similar_sets_log1} <br/>
                            <b>Nome Conjuntos Similares Segundo Arquivo:</b> {item.similar_sets_log2} <br/>
                            <b>Porcentagem Plagio:</b> {item.percent_plagiarism} <br/>
                        </div>
                    )}
                </div>


            </div>
        );
    }
}
