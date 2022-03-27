import { Text, View, Image } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { TextInput, TouchableOpacity } from 'react-native-gesture-handler';
import { useNavigation } from '@react-navigation/native';


import AppLoading from 'expo-app-loading';
import { useState } from 'react';
import { Icon } from 'react-native-elements';
import { theme } from '../utils/theme';

export default function Readings({route}) {
    const navigation = useNavigation();
    const {userid, name} = route.params;
   
    const [heart, setheart] = useState('60');
    const [respiration, setrespiration] = useState('100')
    const [sleep, setsleep] = useState('8')
    const [stress, setstress] = useState('50')
    const [steps, setsteps] = useState('3000')
    const [perspiration, setperspiration] = useState(['40','50'])

   



    return (
    <View style={{backgroundColor:"#fff", flex:1}}>
        <LinearGradient
        colors={['rgb(110, 431, 183)','rgb(86, 230, 253)']}
        style={{height:90, borderBottomRightRadius:20, borderBottomLeftRadius:20}}
        >
            <Text style={{fontWeight:'bold', textAlign:'center', textAlignVertical:'center', marginTop:'10%', fontSize:20,color:"#FFF"}}>Home</Text>
        </LinearGradient>

        <View style={{flexDirection:'row', justifyContent:'space-evenly'}}>
        <LinearGradient
        colors={[ 'rgb(254, 216, 216)','rgb(252, 165, 165)','rgb(252, 165, 165)']}
        style={{height:150, borderRadius:20, width:'45%', marginTop:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg}}>
            <Icon name="heart-pulse" type="material-community" color="#FFF" size={50}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Heart Rate</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{heart}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>BPM</Text>
        </View>
       </LinearGradient>
       <LinearGradient
        colors={['rgb(165, 243, 252)', 'rgb(125, 211, 252)', 'rgb(125, 211, 252)']}
        style={{height:150, borderRadius:20, width:'45%', marginTop:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
            <Icon name="lungs" type="font-awesome-5" color="#FFF" size={40}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Respiration Rate</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{respiration}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>RATE</Text>
        </View>
       </LinearGradient>
       </View>


       <View style={{flexDirection:'row', justifyContent:'space-evenly'}}>
        <LinearGradient
        colors={['rgb(199, 210, 254)', 'rgb(165, 180, 252)', 'rgb(165, 180, 252)']}
        style={{height:150, borderRadius:20, width:'45%', marginVertical:'2.5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg}}>
            <Icon name="power-sleep" type="material-community" color="#FFF" size={45} style={{marginTop:'5%'}}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Sleep</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{sleep}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>HOURS</Text>
        </View>
       </LinearGradient>
       <LinearGradient
        colors={['rgb(254, 215, 170),','rgb(253, 186, 116)', 'rgb(253, 186, 116)']}
        style={{height:150, borderRadius:20, width:'45%', marginVertical:'2.5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
            <Icon name="head-alert" type="material-community" color="#FFF" size={45}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Stress</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{stress}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>RATE</Text>
        </View>
       </LinearGradient>
       </View>

       <LinearGradient
        colors={['rgb(153, 246, 228)', 'rgb(94, 234, 212)', 'rgb(94, 234, 212)']}
        style={{height:150, borderRadius:20, marginVertical:'.5%', marginHorizontal:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
            <Icon name="shoe-prints" type="font-awesome-5" color="#FFF" size={45}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Steps</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{steps}</Text>
        </View>
       </LinearGradient>

       <LinearGradient
        colors={['rgb(191, 219, 254)', 'rgb(147, 197, 253)', 'rgb(147, 197, 253)']}
        style={{height:180, borderRadius:20, marginVertical:'2.5%', marginHorizontal:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
            <Icon name="md-water" type="ionicon" color="#FFF" size={45}></Icon>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Perspiration</Text>
            <View style={{flexDirection:'row', justifyContent:'center'}}>
                <View>
                    <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{perspiration[0]}</Text>
                    <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>RATE</Text>
                </View>
                <View style={{height:50, width:2, backgroundColor:'#EAEAEA', opacity:0.5, marginHorizontal:'5%', marginVertical:'3.5%'}}></View>
                <View>
                    <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{perspiration[1]}</Text>
                    <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>ION LEVEL</Text>
                </View>
            </View>
            </View>
       </LinearGradient>





    </View>
    )
};