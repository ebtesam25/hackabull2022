import { Text, View, Image, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { TextInput, TouchableOpacity } from 'react-native-gesture-handler';
import { useNavigation } from '@react-navigation/native';
import { Modal, Portal, Provider } from 'react-native-paper';
import {
    LineChart,
    BarChart,
    PieChart,
    ProgressChart,
    ContributionGraph,
    StackedBarChart
  } from "react-native-chart-kit";


import AppLoading from 'expo-app-loading';
import { useState } from 'react';
import { Icon } from 'react-native-elements';
import { theme } from '../utils/theme';
import { BlurView } from 'expo-blur';

//Data
import hrateData from '../data/hrate.json';
import respirationData from '../data/respiration.json';
import stepsData from '../data/steps.json';
import stressData from '../data/stress.json';




export default function Home({route}) {
    const [result, setresult] = useState(null);

    const navigation = useNavigation();
    const {userid, name} = route.params;
    const [visible, setVisible] = useState(false);
    const containerStyle = {padding: 20, backgroundColor:'transparent'};
    const [datatype, setdatatype] = useState(null)
    const [secondarydata, setsecondarydata] = useState(null)

    const showModal = () => setVisible(true);
    const hideModal = () => setVisible(false);
   
    const [heart, setheart] = useState('60');
    const [respiration, setrespiration] = useState('100')
    const [sleep, setsleep] = useState('0')
    const [stress, setstress] = useState('50')
    const [steps, setsteps] = useState(stepsData.flatMap((x)=>parseInt(x.steps)).reduce((_sum, a) => _sum + a, 0))
    const [perspiration, setperspiration] = useState(['40','50'])
    const chartConfig = {
        backgroundGradientFrom: "transparent",
        backgroundGradientFromOpacity: 0,
        backgroundGradientTo: "transparent",
        backgroundGradientToOpacity: 0.5,
        color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
        strokeWidth: 2, // optional, default 3
        useShadowColorFromDataset: true // optional
      };

      const _getReadings= (action) =>{
        var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
    
            var raw = JSON.stringify({
            "action": action
            });
    
            var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
            };
    
            fetch("https://gx1znbtqdb.execute-api.us-east-1.amazonaws.com/hackabull2022test", requestOptions)
            .then(response => response.json())
            .then(result => {console.log(result);setresult(result)})
            .catch(error => console.log('error', error));
        }


   



    return (
        <Provider>
      <Portal>
        <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={containerStyle}>
        <BlurView intensity={20} style={{borderRadius:10}} tint="light">
        <LineChart
            withInnerLines={false}
            data={{
            datasets: [
                {
                data: datatype
                },
                {
                data:secondarydata
                }
            ]
            }}
            width={370} // from react-native
            height={550}
            yAxisInterval={1} // optional, defaults to 1
            chartConfig={{
            backgroundColor: theme.primary,
            backgroundGradientFrom: theme.primary,
            backgroundGradientTo: theme.secondary,
            decimalPlaces: 0, // optional, defaults to 2dp
            color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
            style: {
                borderRadius: 10
            },
            propsForDots: {
                r: "1",
                strokeWidth: "2",
                stroke: "#FFF"
            }
            }}
            bezier
            style={{
            borderRadius: 10,
            }}
        />
        
        </BlurView>
        </Modal>
      </Portal>
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
            <TouchableOpacity onPress={()=>{_getReadings("getheartrate");setdatatype(hrateData.heartRateValues.flatMap((x)=>parseInt(x[1])));showModal()}}><Icon name="heart-pulse" type="material-community" color="#FFF" size={50}></Icon></TouchableOpacity>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Heart Rate</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{hrateData.restingHeartRate}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>BPM</Text>
        </View>
       </LinearGradient>
       <LinearGradient
        colors={['rgb(165, 243, 252)', 'rgb(125, 211, 252)', 'rgb(125, 211, 252)']}
        style={{height:150, borderRadius:20, width:'45%', marginTop:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
        <TouchableOpacity onPress={()=>{_getReadings("getrespiration");setdatatype(respirationData.respirationValuesArray.flatMap((x)=>parseInt(x[1])));showModal()}}><Icon name="lungs" type="font-awesome-5" color="#FFF" size={40}></Icon></TouchableOpacity>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Respiration Rate</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{respirationData.avgWakingRespirationValue}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}></Text>
        </View>
       </LinearGradient>
       </View>


       <View style={{flexDirection:'row', justifyContent:'space-evenly'}}>
        <LinearGradient
        colors={['rgb(199, 210, 254)', 'rgb(165, 180, 252)', 'rgb(165, 180, 252)']}
        style={{height:150, borderRadius:20, width:'45%', marginVertical:'2.5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg}}>
        <TouchableOpacity onPress={()=>{_getReadings("getsleep");setdatatype(respirationData.respirationValuesArray.flatMap((x)=>parseInt(x[1])));showModal()}}><Icon name="power-sleep" type="material-community" color="#FFF" size={45} style={{marginTop:'5%'}}></Icon></TouchableOpacity>
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
        <TouchableOpacity onPress={()=>{_getReadings("getstress");setdatatype(stressData.stressValuesArray.flatMap((x)=>parseInt(x[1])));showModal()}}><Icon name="head-alert" type="material-community" color="#FFF" size={45}></Icon></TouchableOpacity>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Stress</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{stressData.avgStressLevel}</Text>
            <Text style={{color:"#FFF", fontSize:10, fontWeight:'bold', textAlign:'center'}}>AVERAGE</Text>
        </View>
       </LinearGradient>
       </View>

       <LinearGradient
        colors={['rgb(153, 246, 228)', 'rgb(94, 234, 212)', 'rgb(94, 234, 212)']}
        style={{height:150, borderRadius:20, marginVertical:'.5%', marginHorizontal:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
        <TouchableOpacity onPress={()=>{showModal()}}><Icon name="shoe-prints" type="font-awesome-5" color="#FFF" size={45}></Icon></TouchableOpacity>
            <Text style={{color:"#FFF", fontSize:15, fontWeight:'bold', textAlign:'center'}}>Steps</Text>
            <Text style={{color:"#FFF", fontSize:40, fontWeight:'bold', textAlign:'center'}}>{steps}</Text>
        </View>
       </LinearGradient>

       <LinearGradient
        colors={['rgb(191, 219, 254)', 'rgb(147, 197, 253)', 'rgb(147, 197, 253)']}
        style={{height:180, borderRadius:20, marginVertical:'2.5%', marginHorizontal:'5%'}}
        >
        <View style={{backgroundColor:theme.secondarybg, marginTop:'5%'}}>
        <TouchableOpacity onPress={()=>{_getReadings("getsweat");setdatatype(result.flatMap((x)=>parseInt(x[1])));setsecondarydata(result.flatMap((x)=>parseInt(x[2])));showModal()}}><Icon name="md-water" type="ionicon" color="#FFF" size={45}></Icon></TouchableOpacity>
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
    </Provider>
    )
};