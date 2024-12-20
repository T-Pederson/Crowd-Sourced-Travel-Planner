import { useState, useEffect } from "react";
import '../css/TripButtons.css';

export default function ExpSaveChanges({ experienceId, experienceName, description, address, latitude, longitude, keywords, photo, onSuccess, onError }){
    const [isLoading, setIsLoading] = useState(false);
    const [isDisabled, setIsDisabled] = useState(true);

    useEffect(() => {
        // Check if all required fields are filled
        if (experienceName && description.trim() && address && latitude && longitude && keywords.length > 0 && photo) {
            setIsDisabled(false);
        } else {
            setIsDisabled(true)
        }
    }, [experienceName, description, address, latitude, longitude, keywords, photo]);

    const handleSave = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/edit_experience` , {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                    Authorization: localStorage.getItem("token")
                },
                body: JSON.stringify({
                    experience_id: experienceId,
                    experience_name: experienceName,
                    description: description,
                    photo: photo,
                    latitude: latitude,
                    longitude: longitude,
                    address: address,
                    keywords: keywords,
                    time_updated: new Date().toISOString()
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to save the experience');
            }
            const data = await response.json();
            onSuccess(data.message);
        } catch (error) {
            onError(error.message);
        }
        finally {
            setIsLoading(false)
        }
    };
    return (
        <div>
          <button onClick={handleSave} disabled={isLoading || isDisabled} className='save-changes'>
            {isLoading ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      ); 
};