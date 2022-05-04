import React, {Component} from "react";


export default class FilesForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            files: true,
        };

    }


    handleRoomButtonPressed(File) {

        //trata o conteudo antes de enviar via json
        //alem do files, ou dentro dele irei ter outros campos
        //como nome do arquivo, conteudo
        //
        // const formData = new FormData();
        // formData.append('image', File)
        print(File)
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                files: this.state.files,
            }),
        };//Talvez isso na hora de redireiconar no meu site, eu ja jogo para o resultado
        fetch("/api/send-files", requestOptions)
            .then((response) => response.json());
    }


    handleChange(event) {
        this.setState({files: event.target.files})
    }

    async handleSubmit(e) {
        print("e: ", e)
        e.preventDefault()
        this.handleRoomButtonPressed(this.state.files);
    }


    async uploadFile(File) {
        const formData = new FormData();
        formData.append('image', File)

        axios.post("/api/send-files", formData, {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }).then(response => {
            console.log(response.data)
        });
    }

    addItem(e) {
        e.preventDefault(); //To prevent the page reload on submit

        var itemArray = this.state.files;

        itemArray.push({
            text: this.refs.inputElement.value
        });

        this.refs.inputElement.value = ""; // clearing the value
    }


    render() {
        return (
            <div>

                <h1>Send Files</h1>


                <form onSubmit={this.addItem.bind(this)}>
                    <input type="file" id="file" multiple name="files"/>
                    <button type="submit" className="btn btn-info"> Update File</button>
                </form>


            </div>
        );
    }
}
