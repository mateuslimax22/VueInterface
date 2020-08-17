import { http } from './config'

export default	{

	resultado:(patient)=>{
		return http.get('Result/'+ patient);
  },
    
	ecgpat:(patient)=>{
		return http.get('Ecg/'+ patient);
  },

    listar:()=>{
		return http.get('Patient')
  },
    
	tempat:(patient)=>{
		return http.get('Temp/'+ patient);
	}
}