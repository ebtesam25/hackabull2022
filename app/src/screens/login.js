import { Text, View, Image } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { TextInput, TouchableOpacity } from 'react-native-gesture-handler';
import { useNavigation } from '@react-navigation/native';


import AppLoading from 'expo-app-loading';
import { useState } from 'react';
import { theme } from '../utils/theme';

export default function Login() {
    const navigation = useNavigation();
   

      const [email, setemail] = useState('');
      const [password, setpassword] = useState('');
      const result = {userid:'1',name:'John Doe'}

      const _loginUser = () => {
        // var myHeaders = new Headers();
        // myHeaders.append("Content-Type", "application/json");
        
        // var raw = JSON.stringify({
        //   "action": "login",
        //   "email": email,
        //   "password": password
        // });
        
        // var requestOptions = {
        //   method: 'POST',
        //   headers: myHeaders,
        //   body: raw,
        //   redirect: 'follow'
        // };
        
        // fetch("https://us-central1-aiot-fit-xlab.cloudfunctions.net/", requestOptions)
        //   .then(response => response.json())
        //   .then(result => {console.log(result); if(result.status=="success"){navigation.navigate('Home',{userid:result.userid, name:result.name})}})
        //   .catch(error => console.log('error', error));
    navigation.navigate('Home',{userid:result.userid, name:result.name})
      }

        return (
    <View style={{backgroundColor:"#000", flex:1}}>
        <LinearGradient
        colors={['rgb(241, 245, 249)','rgb(110, 231, 183)','rgb(186, 230, 253)']}
        style={{flex:1}}
        >
            
   <Image source={require('../assets/logo.png')} style={{alignSelf:'center', marginTop:'15%', width:'50%', height:'15%', resizeMode:'contain', opacity:0.75}}></Image>
    
            <Text style={{fontFamily:'Roboto',textAlign:'center', textAlignVertical:'center', color:theme.primary, fontSize:30, marginBottom:'20%', fontWeight:'bold'}}>SweatSense</Text>

            <View style={{width:'70%', backgroundColor:"#FFF", borderRadius:10, alignSelf:'center', padding:'2.5%', opacity:0.5}}>
                <TextInput placeholder="Email address" style={{fontFamily:'Roboto'}} value={email} onChangeText={(e)=>setemail(e)}></TextInput>
            </View>
            <View style={{width:'70%', backgroundColor:"#FFF", borderRadius:10, alignSelf:'center', padding:'2.5%', opacity:0.5, marginVertical:'5%'}}>
                <TextInput placeholder="Password" secureTextEntry style={{fontFamily:'Roboto'}} value={password} onChangeText={(e)=>setpassword(e)}></TextInput>
            </View>

            <TouchableOpacity onPress={()=>_loginUser()}>
                <View style={{ borderRadius:10,width:150, height:50, alignSelf:'center', backgroundColor:"#FFF", justifyContent:'center', elevation:1}}><Text style={{fontFamily:'Roboto',textAlign:'center', textAlignVertical:'center', color:theme.primary, fontSize:15, fontWeight:'bold'}}>LOGIN</Text>
        </View></TouchableOpacity>
        </LinearGradient>
    </View>
    )
};