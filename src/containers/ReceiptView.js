import React from "react";
import axios from "axios";
import CustomForm from "../components/Form";


class ReceiptV extends React.Component {
  state = {
    receipts: []
  };

  fetchReceipts = () => {
    axios.get("http://127.0.0.1:8000/receipts/").then(res => {
      this.setState({
        receipts: res.data
      });
    });
  }

  componentDidMount() {
    this.fetchReceipts();
  }

  componentWillReceiveProps(newProps) {
    if (newProps.token) {
      this.fetchReceipts();      
    }
  }

  render() {
    return (
      <div>
        <Receipts data={this.state.receipts} /> <br />
        <h2> Post a receipt </h2>
        <CustomForm requestType="post" articleID={null} btnText="Create" />
      </div>
    );
  }
}

export default ReceiptV;