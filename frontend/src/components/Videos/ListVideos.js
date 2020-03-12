import React, {Component} from "react";

class ListVideos extends Component {
    constructor(props) {
        super(props);

        this.state={
            objGroup: {}
        }
    }


    static getDerivedStateFromProps(nextProps, prevState){

        if(nextProps.apiData!== prevState.apiData){
            let objGroup={};
            nextProps.apiData.forEach(item=> {
                objGroup[item.channel.name]= objGroup[item.channel.name] || [];
                objGroup[item.channel.name].push(item)
            });
            return { objGroup: objGroup};
        }
        else return null;
    }

    // componentDidUpdate(prevProps, prevState) {
    //     debugger
    //     if(prevProps.apiData!==this.props.apiData){
    //         //Perform some operation here
    //         this.setState({objGroup: this.props.apiData});
    //     }
    // }

    render() {
        const results = Object.keys(this.state.objGroup).map((key, index) =>
            <div key={index}><h1><b>Channel {key}</b></h1>
                {this.state.objGroup[key].map((items, idx) =>
                    <p key={idx}><b> Title video: {items.title} - Create date: {items.create_date} </b>
                        {items.measurements.map((val, idx) =>
                            <p key={idx}>measurement: {val.measurement_date}</p>
                        )}
                    </p>
                )}
            </div>,
        );
        return <div>{results}</div>
    }
}

export default ListVideos;