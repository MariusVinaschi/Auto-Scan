import React from 'react'; 
import TemplatePage from './TemplatePage';

import BoxContainer from '../Component/BoxContainer'; 
import User from '../Component/Profile/User';

const Profile = () => {
    return (
        <TemplatePage>
            <BoxContainer title='User Information'>
                <User /> 
            </BoxContainer>            
        </TemplatePage>
    )
}

export default Profile

