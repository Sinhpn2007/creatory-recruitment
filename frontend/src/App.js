import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ListVideos from "./components/Videos/ListVideos";


function App() {
    // We like to use axios for fetching from the backend
    // but feel free to use something else if you prefer that!


    // eslint-disable-next-line
    const [apiData, setApiData] = useState([]);
    // eslint-disable-next-line
    const [isLoading, setIsLoading] = useState(true);
    // eslint-disable-next-line
    const [isError, setIsError] = useState(false);

    useEffect(() => {
        // setApiData([1, 2]);
        const fetchData = async () => {
            setIsLoading(true);
            setIsError(false);
            try {
                const result = await axios.get(
                    '/results'
                );
                setIsLoading(false);
                setApiData(result.data);
            }
            catch (error) {
                setIsLoading(false);
                setIsError(true);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="App">
            <ListVideos apiData={apiData.list_video} test="123124"/>
        </div>
    );
}

export default App;
