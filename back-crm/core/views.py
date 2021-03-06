
from rest_framework import viewsets
from .serializers import ClienteSerializer, EstagioSerializer, OrganizacaoSerializer, ProdutoSerializer, TicketSerializer, VendedorSerializer, ErpSerializer, RamoSerializer, AtividadeSerializer, UserSerializer, ObsSerializer, VendedorExtSerializer
from .models import Cliente, Estagio, Organizacao, Produto, Ticket, Vendedor, Atividade, Created, Updated, Erp, Ramo, Obs, VendedorExt, File
from django.core import serializers
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request):
        data = request.data
        print('received data:', data)

        return JsonResponse({"message": "successs"})


class ObsViewSet(viewsets.ModelViewSet):
    queryset = Obs.objects.all().order_by('-id')
    serializer_class = ObsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RamoViewSet(viewsets.ModelViewSet):

    queryset = Ramo.objects.all().order_by('-id')
    serializer_class = RamoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        print(data)
        r = Ramo()
        c = Created()
        c.user = request.user
        c.save()
        r.desc = data['desc']
        r.created = c
        r.save()
        return JsonResponse({'messsage': 'worked'})


class ErpViewSet(viewsets.ModelViewSet):

    queryset = Erp.objects.all().order_by('-id')
    serializer_class = ErpSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        print(data)
        c = Created()
        c.user = request.user
        c.save()
        e = Erp()
        e.codigo = data['codigo']
        e.desc = data['desc']
        e.empresa = data['empresa']
        e.save()

        return JsonResponse({'messsage': 'worked'})


class ClienteViewSet(viewsets.ModelViewSet):

    queryset = Cliente.objects.all().order_by('-id')
    serializer_class = ClienteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data

        create = Created()
        create.user = request.User
        create.save()

        C = Cliente()
        C.nome = data['nome']
        C.tipo = data['tipo']
        C.fone = data['fone']
        C.celular = data['celular']
        C.email = data['email']
        C.skype = data['skype']
        # C.org = Organizacao.objects.get(id=data['org'])
        C.created = create
        C.save()
        print(data)
        return JsonResponse({'message': 'Worked'})


class EstagioViewSet(viewsets.ModelViewSet):

    queryset = Estagio.objects.all()
    serializer_class = EstagioSerializer


class OrganizacaoViewSet(viewsets.ModelViewSet):

    queryset = Organizacao.objects.all().order_by('-id')
    serializer_class = OrganizacaoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        print(request.user)

        print('chamou request')
        print(data)

        cr = Created()
        cr.user = request.user
        cr.save()

        C = Organizacao()
        C.codigo = data['codigo']
        C.razaosocial = data['razaosocial']
        C.nomefantasia = data['nomefantasia']
        C.telefone = data['telefone']
        C.rua = data['rua']
        C.complemento = data['complemento']
        C.bairro = data['bairro']
        C.cep = data['cep']
        C.cidade = data['cidade']
        C.uf = data['uf']
        C.created = cr
        try:
            C.email = data['email']
            C.site = data['site']
        except:
            pass
        try:
            C.cnpj = data['cnpj']
        except:
            pass
        try:
            C.ramo = Ramo.objects.get(id=int(data['ramos']))
        except:
            pass
        C.ie = data['ie']
        try:
            C.erpe = Erp.objects.get(id=int(data['erp']))
        except:
            pass
        C.save()
        contatos = data['contatos']
        for i in contatos:
            print('CONTATOS : ', i)

            o = Cliente()
            cr = Created()
            cr.user = request.user
            cr.save()
            o.nome = i['nome']
            o.email = i['email']
            o.cargo = i['cargo']
            o.dep = i['dep']
            o.birth = i['birth']
            o.tel = i['tel']
            o.ramal = i['ramal']
            o.cel = i['cel']
            o.skype = i['skp']
            o.created = cr
            o.save()
            C.contatos.add(o)
            C.save()

        print(data)
        return JsonResponse({'message': 'Worked'})

    def update(self, request, pk):
        data = request.data
        print(data)

        O = Organizacao.objects.get(id=int(data['id']))
        O.codigo = data['codigo']
        O.razaosocial = data['razaosocial']
        O.nomefantasia = data['nomefantasia']
        O.telefone = data['telefone']
        O.rua = data['rua']
        O.complemento = data['complemento']
        O.bairro = data['bairro']
        O.cep = data['cep']
        O.cidade = data['cidade']
        O.uf = data['uf']
        try:
            O.email = data['email']
            O.site = data['site']
        except:
            pass
        try:
            O.cnpj = data['cnpj']
        except:
            pass
        try:
            O.ramo = Ramo.objects.get(id=int(data['ramos']))
        except:
            pass
        try:
            O.erpe = Erp.objects.get(id=int(data['erp']))
        except:
            pass

        O.ie = data['ie']
        O.save()

        O.contatos.clear()
        contatos = data['contatos']
        for i in contatos:
            print('CONTATOS : ', i)

            o = Cliente()
            o.nome = i['nome']
            o.email = i['email']
            o.cargo = i['cargo']
            o.dep = i['dep']
            o.birth = i['birth']
            o.tel = i['tel']
            o.cel = i['cel']
            try:
                o.skype = i['skype']
            except:
                o.skype = i['skp']
            o.save()
            O.contatos.add(o)
            O.save()
        return JsonResponse({'message': 'Worked'})


class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = Produto.objects.all().order_by('-id')
    serializer_class = ProdutoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        print(data)
        c = Created()
        c.user = request.user
        c.save()
        p = Produto()
        p.nome = data['nome']
        p.codigo = data['codigo']
        p.created = c
        p.save()

        return JsonResponse({'message': 'worked'})


class VendedorExtViewSet(viewsets.ModelViewSet):

    queryset = VendedorExt.objects.all().order_by('-id')
    serializer_class = VendedorExtSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all().order_by('-id')
    serializer_class = TicketSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data

        print(data['titulo'])
        print(request.user)
        print(request.headers)

        f = File()
        f.titulo = data['titulo']
        f.file = data['file']
        f.save()

        c = Created()
        c.user = request.user
        c.save()
        V = Vendedor.objects.get(id=int(data['vendedor']))
        print(V)

        T = Ticket()
        T.titulo = data['titulo']
        T.estagio = Estagio.objects.get(id=int(data['estagio']))
        T.cliente = Cliente.objects.get(id=int(data['cliente']))
        T.org = Organizacao.objects.get(id=int(data['org']))
        T.valorestimado = int(data['valorestimado'])
        T.termometro = data['termometro']
        T.vendedor = V
        T.status = 'Aberto'

        T.created = c
        T.save()
        try:
            if data['obs'].length >= 1:
                for i in data['obs']:
                    c = Created()
                    c.user = request.user
                    c.save()
                    k = Obs()
                    k.texto = i
                    k.created = c
                    k.save()
                    T.obs.add(k)
                    T.save()
        except:
            k = Obs()
            c = Created()
            c.user = request.user
            c.save()
            k.texto = data['obs']
            k.created = c
            k.save()
            T.obs.add(k)
            T.save()

        produtos = data['produto']
        for prod in produtos:
            T.produto.add(Produto.objects.get(id=prod))

        T.file.add(f)
        T.save()
        print(data)
        return JsonResponse({'message': 'Saved'})

    def update(self, request, pk):
        data = request.data
        print(data)

        try:
            T = Ticket.objects.get(id=data['id'])
            c = Created()
            c.user = request.user
            c.save()
            f = File()
            f.titulo = data['filetitle']
            f.file = data['files']
            f.created = c
            f.save()
            T.file.add(f)
            T.save()
        except:
            pass

        try:
            T = Ticket.objects.get(id=data['id'])
            T.estagio = Estagio.objects.get(id=data['estagio'])
            T.status = data['status']
            if T.status == 'Perdido':
                T.mtvperd = data['mtvperd']
                T.cmtperd = data['cmtperd']
            T.save()
        except:
            pass

        try:
            if data['title']:
                print("VALORRECEBIDO: ", data['value'])
                id = data['id']
                T = Ticket.objects.get(id=data['id'])
                T.titulo = data['title']
                T.valorestimado = int(data['value'])
                try:
                    C = Cliente.objects.get(id=int(data['contact']['id']))
                except:
                    pass
                T.cliente = C
                T.save()

        except:
            pass

        try:
            if data['opt'] == 'term':
                print('entrou opt ')

                T = Ticket.objects.get(id=data['id'])
                T.termometro = data['term']
                T.save()
        except:
            pass

        try:
            if data['opt'] == 'obs':
                o = Obs()
                c = Created()
                c.user = request.user
                c.save()
                o.created = c
                o.texto = data['obs']
                o.save()
                T = Ticket.objects.get(id=data['id'])
                T.obs.add(o)
                T.save()
        except:
            pass

        return JsonResponse({'message': 'Updated'})


class VendedorViewSet(viewsets.ModelViewSet):

    queryset = Vendedor.objects.all().order_by('-id')
    serializer_class = VendedorSerializer


class AtividadeViewSet(viewsets.ModelViewSet):

    queryset = Atividade.objects.all().order_by('id')
    serializer_class = AtividadeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        print('CREATING')
        print(data)

        V = Vendedor.objects.get(id=int(data['vendedor']['id']))

        c = Created()
        c.user = request.user
        c.save()
        A = Atividade()
        A.dataini = data['dataini']
        A.datafim = data['datafim']
        A.horaini = data['horaini']
        A.horafim = data['horafim']
        A.assunto = data['assunto']
        A.feito = False
        A.vendedor = V
        A.ticket = Ticket.objects.get(id=int(data['ticket']))
        A.cliente = Cliente.objects.get(id=int(data['cliente']['id']))
        A.org = Organizacao.objects.get(id=int(data['org']['id']))
        A.tipo = data['tipo']
        A.created = c
        A.save()
        return JsonResponse({'message': 'atividadecreated'})

    def update(self, request, pk):
        data = request.data
        print(data)
        try:
            if data['id']:
                print(data)

                A = Atividade.objects.get(id=data['id'])
                A.feito = data['feito']
                A.save()
                print('entrouaqui')

        except:
            print(data)

            A = Atividade.objects.get(id=data['position'])
            A.dataini = data['dataini']
            A.datafim = data['datafim']
            A.horaini = data['horaini']
            A.horafim = data['horafim']
            A.assunto = data['assunto']
            print(data['vendedor'])
            V = Vendedor.objects.get(id=int(data['vendedor']['id']))
            A.vendedor = V
            A.feito = data['feito']
            print('CLIENTE: ', data['cliente'])
            print('ORG: ', data['org'])

            A.ticket = Ticket.objects.get(id=int(data['ticket']))
            A.cliente = Cliente.objects.get(id=int(data['cliente']['id']))
            A.org = Organizacao.objects.get(id=int(data['org']['id']))
            A.tipo = data['tipo']
            A.save()

        return JsonResponse({'message': 'atividadesupdated'})
