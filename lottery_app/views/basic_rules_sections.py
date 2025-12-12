from rest_framework.views import APIView
from rest_framework.response import Response
from lottery_app.models import *
from lottery_app.serializers import *
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework import status
from lottery_web_app.serializers import *

# basic rules for price claim, create and list 
class BasicRulesSectionsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rules = PriceClaimRule.objects.all().order_by('order')
        serializer = PriceClaimRulesSerializer(rules, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
    
    def post(self, request):
        serializer = PriceClaimRulesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response({
                "success": True,
                "message": "Rule created successfully",
                "data": serializer.data
            }, status=201)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response
    


# basic rules section patch api delete apis 
class BasicRulesSectionEditDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return PriceClaimRule.objects.get(pk=pk)
        except PriceClaimRule.DoesNotExist:
            return None

    def patch(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            response =  Response({
                "success": False,
                "message": "Rule not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        serializer = PriceClaimRulesSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response =  Response({
                "success": True,
                "message": "Rule updated successfully",
                "data": serializer.data
            }, status=200)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response

    def delete(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            response =  Response({
                "success": False,
                "message": "Rule not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        rule.delete()
        response =  Response({
            "success": True,
            "message": "Rule deleted successfully"
        }, status=200)
        response.encrypt_payload = True
        return response
    


# documents required for price claim section
class DocumentsRequiredPriceClaimView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        documents = DocumentsRequiredForPrizeClaim.objects.all()
        serializer = DocumentsRequiredSerializer(documents, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
    def post(self,request):
        serializer = DocumentsRequiredSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response({
                "success": True,
                "message": "Document created successfully",
                "data": serializer.data
            }, status=201)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response
    


# documents reuired for price claim edit delete api
class DocumentsRequiredPriceClaimEditDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return DocumentsRequiredForPrizeClaim.objects.get(pk=pk)
        except DocumentsRequiredForPrizeClaim.DoesNotExist:
            return None

    def patch(self, request, pk):
        document = self.get_object(pk)
        if not document:
            response =  Response({
                "success": False,
                "message": "Document not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        serializer = DocumentsRequiredSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response =  Response({
                "success": True,
                "message": "Document updated successfully",
                "data": serializer.data
            }, status=200)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response

    def delete(self, request, pk):
        document = self.get_object(pk)
        if not document:
            response =  Response({
                "success": False,
                "message": "Document not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        document.delete()
        response =  Response({
            "success": True,
            "message": "Document deleted successfully"
        }, status=200)
        response.encrypt_payload = True
        return response    
    

# impotent reminders and help and support can be added similarly if needed
class ImportentRemindersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reminders = ImportentReminders.objects.all()
        serializer = ImportentRemindersSerializer(reminders, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
    
    def post(self, request):
        serializer = ImportentRemindersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response({
                "success": True,
                "message": "Reminder created successfully",
                "data": serializer.data
            }, status=201)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response
    

 # edit delete important reminders 
class EditDeleteImportentRemindersAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return ImportentReminders.objects.get(pk=pk)
        except ImportentReminders.DoesNotExist:
            return None

    def patch(self, request, pk):
        reminder = self.get_object(pk)
        if not reminder:
            response =  Response({
                "success": False,
                "message": "Reminder not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        serializer = ImportentRemindersSerializer(reminder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response =  Response({
                "success": True,
                "message": "Reminder updated successfully",
                "data": serializer.data
            }, status=200)
            response.encrypt_payload = True
            return response
        response =  Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        response.encrypt_payload = True
        return response

    def delete(self, request, pk):
        reminder = self.get_object(pk)
        if not reminder:
            response =  Response({
                "success": False,
                "message": "Reminder not found"
            }, status=404)
            response.encrypt_payload = True
            return response

        reminder.delete()
        response =  Response({
            "success": True,
            "message": "Reminder deleted successfully"
        }, status=200)
        response.encrypt_payload = True
        return response   
    


class LotteryInfoList(APIView):
    def get(self, request):
        queryset = LotteryInfo.objects.all()
        serializer = LotteryInfoSerializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
class AccountSupportList(APIView):
    def get(self, request):
        queryset = AccountSupport.objects.all()
        serializer = AccountSupportSerializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)   
        
        
        
class Weekly_Schedule_List(APIView):
    def get(self, request):
        queryset = WeeklySchedule.objects.all()
        serializer =Weekly_ScheduleSerializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)      
        
        
        
class ImportantRule_List(APIView):
    def get(self, request):
        queryset = ImportantRule.objects.all()
        serializer =ImportantRule_Serializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)         
        
        
        
        
        
class SaftyRule_List(APIView):
    def get(self, request):
        queryset = SafetyRule.objects.all()
        serializer =SafetyRule_Serializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)                
              
              
              
class OfficialResource_List(APIView):
    def get(self, request):
        queryset = OfficialResource.objects.all()
        serializer =OfficialResourceSerializer(queryset, many=True)

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)    
    


# terms and condition adding listing apis 


class TermsAndConditionAddListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        terms = TermsAndConditions.objects.all().order_by('-created_at')
        serializer = TermsAndConditionsSerializer(terms, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
    
    def post(self, request):
        existing_terms = TermsAndConditions.objects.first()

        if existing_terms:
         
            serializer = TermsAndConditionsSerializer(
                existing_terms,
                data=request.data,
                partial=True  
            )
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Terms and Conditions updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = TermsAndConditionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Terms and Conditions created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    



    # edit , delete api 
class TermsAndConditionsEditDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return TermsAndConditions.objects.get(pk=pk)
        except TermsAndConditions.DoesNotExist:
            return None

    def patch(self, request, pk):
        terms = self.get_object(pk)
        if not terms:
            Response({
                "success": False,
                "message": "Terms and Conditions not found"
            }, status=404)
            # response.encrypt_payload = True
            # return response

        serializer = TermsAndConditionsSerializer(terms, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            Response({
                "success": True,
                "message": "Terms and Conditions updated successfully",
                "data": serializer.data
            }, status=200)
            # response.encrypt_payload = True
            # return response
        Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
        # response.encrypt_payload = True
        # return response

    def delete(self, request, pk):
        terms = self.get_object(pk)
        if not terms:
            Response({
                "success": False,
                "message": "Terms and Conditions not found"
            }, status=404)
         

        terms.delete()
        Response({
            "success": True,
            "message": "Terms and Conditions deleted successfully"
        }, status=200)
   

# privacy policy add and list api
class PrivacyPolicyAddListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self , request):
        policies = PrivacyPolicy.objects.all().order_by('-created_at')
        serializer = PrivacyPolicySerializer(policies, many=True)
        response = Response({
            "success": True,
            "data": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
    
    def post(self, request):
        existing_privacy = PrivacyPolicy.objects.first()

        if existing_privacy:
            serializer = PrivacyPolicySerializer(
                existing_privacy,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Privacy Policy updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


        serializer = PrivacyPolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Privacy Policy created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




# privacy policy edit delete api
class PrivacyPolicyEditDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return PrivacyPolicy.objects.get(pk=pk)
        except PrivacyPolicy.DoesNotExist:
            return None

    def patch(self, request, pk):
        policy = self.get_object(pk)
        if not policy:
            return Response({
                "success": False,
                "message": "Privacy Policy not found"
            }, status=404)
        

        serializer = PrivacyPolicySerializer(policy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Privacy Policy updated successfully",
                "data": serializer.data
            }, status=200)
      
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
  

    def delete(self, request, pk):
        policy = self.get_object(pk)
        if not policy:
            return Response({
                "success": False,
                "message": "Privacy Policy not found"
            }, status=404)
          

        policy.delete()
        return Response({
            "success": True,
            "message": "Privacy Policy deleted successfully"
        }, status=200)
    

class LotteryInfoAdd(APIView):
    def post(self, request):
        serializer = LotteryInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Lottery Info created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------
# EDIT LOTTERY INFO (PUT)
# -------------------------------------------------
class LotteryInfoEdit(APIView):
    def put(self, request, pk):
        try:
            obj = LotteryInfo.objects.get(id=pk)
        except LotteryInfo.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lottery info not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = LotteryInfoSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Lottery info updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------
# DELETE LOTTERY INFO (DELETE)
# -------------------------------------------------
class LotteryInfoDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = LotteryInfo.objects.get(id=pk)
        except LotteryInfo.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lottery info not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Lottery info deleted successfully"
        }, status=status.HTTP_200_OK)
        
        
        
class AccountSupportAdd(APIView):
    def post(self, request):
        serializer = AccountSupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Account support info added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class AccountSupportEdit(APIView):
    def put(self, request, pk):
        try:
            obj = AccountSupport.objects.get(id=pk)
        except AccountSupport.DoesNotExist:
            return Response({
                "success": False,
                "message": "Account support info not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSupportSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Account support info updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------
# DELETE (DELETE)
# -----------------------------------------
class AccountSupportDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = AccountSupport.objects.get(id=pk)
        except AccountSupport.DoesNotExist:
            return Response({
                "success": False,
                "message": "Account support info not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Account support info deleted successfully"
        }, status=status.HTTP_200_OK)
        
        
        
class add_Weekly_Schedule(APIView):
    def post(self, request):
        serializer = Weekly_ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "weekely schedule added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
    
    
class Weekly_ScheduleEdit(APIView):
    def put(self, request, pk):
        try:
            obj = WeeklySchedule.objects.get(id=pk)
        except WeeklySchedule.DoesNotExist:
            return Response({
                "success": False,
                "message": "WeeklySchedule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = Weekly_ScheduleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "WeeklySchedule  updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class Weekly_ScheduleDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = WeeklySchedule.objects.get(id=pk)
        except WeeklySchedule.DoesNotExist:
            return Response({
                "success": False,
                "message": "WeeklySchedule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "WeeklySchedule  deleted successfully"
        }, status=status.HTTP_200_OK)  
        
        
        
class add_ImportantRule(APIView):
    def post(self, request):
        serializer = ImportantRule_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "ImportantRule added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    
    
    
class ImportantRuleEdit(APIView):
    def put(self, request, pk):
        try:
            obj = ImportantRule.objects.get(id=pk)
        except ImportantRule.DoesNotExist:
            return Response({
                "success": False,
                "message": "ImportantRule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ImportantRule_Serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "ImportantRule  updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ImportantRuleDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = ImportantRule.objects.get(id=pk)
        except ImportantRule.DoesNotExist:
            return Response({
                "success": False,
                "message": "ImportantRule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "ImportantRule  deleted successfully"
        }, status=status.HTTP_200_OK)  
        
        
        
        
class add_SafetyRule(APIView):
    def post(self, request):
        serializer = SafetyRule_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "SafetyRule added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    
class SafetyRuleEdit(APIView):
    def put(self, request, pk):
        try:
            obj = SafetyRule.objects.get(id=pk)
        except SafetyRule.DoesNotExist:
            return Response({
                "success": False,
                "message": "SafetyRule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SafetyRule_Serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "SafetyRule updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
    
class SafetyRuleDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = SafetyRule.objects.get(id=pk)
        except SafetyRule.DoesNotExist:
            return Response({
                "success": False,
                "message": "SafetyRule  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "ImportantRule  deleted successfully"
        }, status=status.HTTP_200_OK)     
        
        
        
class OfficialResourceAdd(APIView):
    def post(self, request):
        serializer = OfficialResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Official resource added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class OfficialResourceEdit(APIView):
    def put(self, request, pk):
        try:
            obj = OfficialResource.objects.get(id=pk)
        except OfficialResource.DoesNotExist:
            return Response({
                "success": False,
                "message": "OfficialResource not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OfficialResourceSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "OfficialResource updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
class OfficialResourceDelete(APIView):
    def delete(self, request, pk):
        try:
            obj = OfficialResource.objects.get(id=pk)
        except OfficialResource.DoesNotExist:
            return Response({
                "success": False,
                "message": "OfficialResource  not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "OfficialResource deleted successfully"
        }, status=status.HTTP_200_OK)   
        
        
        
        
class GeneralHelpListCreate(APIView):
    def get(self, request):
        objs = GeneralHelp.objects.all().order_by("id")
        serializer = GeneralHelpSerializer(objs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = GeneralHelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "General help section added",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  
        
        
class GeneralHelpEditDelete(APIView):
    def put(self, request, pk):
        try:
            obj = GeneralHelp.objects.get(id=pk)
        except GeneralHelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = GeneralHelpSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = GeneralHelp.objects.get(id=pk)
        except GeneralHelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Deleted successfully"
        })
        
        
        
class AccountsupporthelpListCreate(APIView):
    def get(self, request):
        objs = accountsupporthelp.objects.all().order_by("id")
        serializer = AccountsupporthelpSerializer(objs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = AccountsupporthelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Accountsupport help section added",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  
        
        
        
        
class AccountsupporthelpEditDelete(APIView):
    def put(self, request, pk):
        try:
            obj = accountsupporthelp.objects.get(id=pk)
        except accountsupporthelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountsupporthelpSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = accountsupporthelp.objects.get(id=pk)
        except accountsupporthelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Deleted successfully"
        }) 
        
        
        
class paymentandsubscriptionhelpListCreate(APIView):

    def get(self, request):
        objs = paymentandsubscriptionhelp.objects.all().order_by("id")
        serializer = paymentandsubscriptionhelpSerializer(objs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = paymentandsubscriptionhelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Payment & Subscription help section added",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class paymentandsubscriptionhelpEditDelete(APIView):
    def put(self, request, pk):
        try:
            obj = paymentandsubscriptionhelp.objects.get(id=pk)
        except paymentandsubscriptionhelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = paymentandsubscriptionhelpSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Updated successfully",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = paymentandsubscriptionhelp.objects.get(id=pk)
        except paymentandsubscriptionhelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Deleted successfully"
        })
        
        
        
class PurchaseLotteryHelpListCreate(APIView):
    def get(self, request):
        objs = purchaselotteryhelp.objects.all().order_by("id")
        serializer = PurchaseLotteryHelpSerializer(objs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def post(self, request):
        serializer = PurchaseLotteryHelpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Purchase Lottery Help added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)    
        
        
class PurchaseLotteryHelpEditDelete(APIView):
    def put(self, request, pk):
        try:
            obj = purchaselotteryhelp.objects.get(id=pk)
        except purchaselotteryhelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseLotteryHelpSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Purchase Lottery Help updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = purchaselotteryhelp.objects.get(id=pk)
        except purchaselotteryhelp.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Purchase Lottery Help deleted successfully"
        })
        
        
        
        
class ContactSupportListCreate(APIView):
    def get(self, request):
        objs = ContactSupport.objects.all().order_by("id")
        serializer = ContactSupportSerializer(objs, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def post(self, request):
        # Check if record already exists
        existing = ContactSupport.objects.first()

        if existing:
            # Update the existing record
            serializer = ContactSupportSerializer(existing, data=request.data)
        else:
            # Create new record
            serializer = ContactSupportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Details saved successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class ContactSupportEditDelete(APIView):
    def put(self, request, pk):
        try:
            obj = ContactSupport.objects.get(id=pk)
        except ContactSupport.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSupportSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = ContactSupport.objects.get(id=pk)
        except ContactSupport.DoesNotExist:
            return Response({
                "success": False,
                "message": "Record not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response({
            "success": True,
            "message": "Deleted successfully"
        })
